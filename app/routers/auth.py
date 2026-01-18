from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserLogin, UserRegister
from app.security import SessionManager, CSRFProtection, verify_csrf, get_current_user_id

router = APIRouter()
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Display login page"""
    csrf_token = CSRFProtection.generate_csrf_token()
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "csrf_token": csrf_token,
            "page": "login"
        }
    )


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle login submission"""
    verify_csrf(request, csrf_token)
    
    user = db.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    session_token = SessionManager.create_session_token(user.id)
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax"
    )
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Display registration page"""
    csrf_token = CSRFProtection.generate_csrf_token()
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "csrf_token": csrf_token,
            "page": "register",
            "is_register": True
        }
    )


@router.post("/register")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(None),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle registration submission"""
    verify_csrf(request, csrf_token)
    
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    password_hash = pwd_context.hash(password)
    user = User(
        email=email,
        password_hash=password_hash,
        full_name=full_name
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    session_token = SessionManager.create_session_token(user.id)
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return response


@router.get("/logout")
async def logout(request: Request):
    """Handle logout"""
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session_token")
    return response
