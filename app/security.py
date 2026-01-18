import secrets
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config import settings
from app.db import get_db

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# CSRF protection
csrf_serializer = URLSafeTimedSerializer(settings.secret_key)

# JWT bearer token
security_bearer = HTTPBearer()

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.effective_jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(token, settings.effective_jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_bearer), db: Session = Depends(get_db)):
    """Dependency to get the current authenticated user from JWT token"""
    from app.models.user import User
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_active_user(current_user = Depends(get_current_user)):
    """Dependency to get current active user"""
    return current_user

def require_role(role: str):
    """Dependency factory to require a specific role"""
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have required role: {role}"
            )
        return current_user
    return role_checker

# CSRF token utilities
def generate_csrf_token() -> str:
    return csrf_serializer.dumps(secrets.token_urlsafe(16))

def verify_csrf_token(token: str, max_age: int = 60 * 60 * 2):
    try:
        csrf_serializer.loads(token, max_age=max_age)
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid CSRF token")

def get_session_csrf(request: Request) -> str:
    token = request.session.get("csrf")
    if not token:
        token = generate_csrf_token()
        request.session["csrf"] = token
    return token

def require_csrf(request: Request):
    token = request.headers.get("X-CSRF-Token")
    if not token:
        raise HTTPException(status_code=403, detail="Missing CSRF token")
    verify_csrf_token(token)
    return True

# Legacy session-based auth (kept for compatibility)
def require_auth(request: Request):
    if not request.session.get("user_id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return request.session