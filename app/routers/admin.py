from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.security import require_auth, CSRFProtection

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def admin_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """Admin dashboard"""
    user_id = require_auth(request)
    
    # Check if user is admin
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_admin:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": "Access denied. Admin privileges required."
            },
            status_code=403
        )
    
    # Get statistics
    total_users = db.query(User).count()
    
    csrf_token = CSRFProtection.generate_csrf_token()
    
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "total_users": total_users,
            "csrf_token": csrf_token,
            "page": "admin"
        }
    )
