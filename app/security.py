import secrets
from itsdangerous import URLSafeTimedSerializer
from fastapi import Request, HTTPException, status, Depends
from app.config import settings

csrf_serializer = URLSafeTimedSerializer(settings.secret_key)

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

def require_auth(request: Request):
    if not request.session.get("user_id"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return request.session

def require_role(role: str):
    def checker(session=Depends(require_auth)):
        if session.get("role") != role:
            raise HTTPException(status_code=403, detail="Forbidden")
        return session
    return checker