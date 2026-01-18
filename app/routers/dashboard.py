from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.security import require_auth, CSRFProtection

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    """User dashboard"""
    user_id = require_auth(request)
    user = db.query(User).filter(User.id == user_id).first()
    
    csrf_token = CSRFProtection.generate_csrf_token()
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "csrf_token": csrf_token,
            "page": "dashboard"
        }
    )
