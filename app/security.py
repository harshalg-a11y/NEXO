from typing import Optional
import secrets
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import Request, HTTPException, status
from app.config import get_settings

settings = get_settings()


class SessionManager:
    """Simple session manager using signed cookies"""
    
    @staticmethod
    def create_session_token(user_id: int) -> str:
        """Create a signed session token"""
        serializer = URLSafeTimedSerializer(settings.session_secret_key)
        return serializer.dumps({"user_id": user_id})
    
    @staticmethod
    def verify_session_token(token: str) -> Optional[dict]:
        """Verify and decode session token"""
        serializer = URLSafeTimedSerializer(settings.session_secret_key)
        try:
            data = serializer.loads(token, max_age=settings.session_max_age)
            return data
        except (BadSignature, SignatureExpired):
            return None


class CSRFProtection:
    """CSRF token generation and validation"""
    
    @staticmethod
    def generate_csrf_token() -> str:
        """Generate a CSRF token"""
        serializer = URLSafeTimedSerializer(settings.csrf_secret_key)
        return serializer.dumps({"csrf": secrets.token_hex(32)})
    
    @staticmethod
    def verify_csrf_token(token: str) -> bool:
        """Verify CSRF token"""
        serializer = URLSafeTimedSerializer(settings.csrf_secret_key)
        try:
            serializer.loads(token, max_age=3600)  # 1 hour expiry
            return True
        except (BadSignature, SignatureExpired):
            return False


def get_current_user_id(request: Request) -> Optional[int]:
    """Get current user ID from session cookie"""
    session_token = request.cookies.get("session_token")
    if not session_token:
        return None
    
    session_data = SessionManager.verify_session_token(session_token)
    if not session_data:
        return None
    
    return session_data.get("user_id")


def require_auth(request: Request) -> int:
    """Require authentication, raise 401 if not authenticated"""
    user_id = get_current_user_id(request)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return user_id


def verify_csrf(request: Request, csrf_token: str) -> None:
    """Verify CSRF token from form or header"""
    if not csrf_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token missing"
        )
    
    if not CSRFProtection.verify_csrf_token(csrf_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid CSRF token"
        )
