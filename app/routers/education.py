from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.security import require_auth, CSRFProtection

router = APIRouter(prefix="/education")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def education_page(request: Request):
    """Education resources page"""
    user_id = require_auth(request)
    
    csrf_token = CSRFProtection.generate_csrf_token()
    
    # Stub educational content
    courses = [
        {"id": 1, "title": "Basic Agriculture", "description": "Learn farming basics"},
        {"id": 2, "title": "Health & Wellness", "description": "Health education"},
        {"id": 3, "title": "Financial Literacy", "description": "Money management"},
    ]
    
    return templates.TemplateResponse(
        "education.html",
        {
            "request": request,
            "courses": courses,
            "csrf_token": csrf_token,
            "page": "education"
        }
    )
