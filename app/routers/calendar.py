from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.security import require_auth, CSRFProtection

router = APIRouter(prefix="/calendar")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def calendar_page(request: Request):
    """Calendar/scheduling page"""
    user_id = require_auth(request)
    
    csrf_token = CSRFProtection.generate_csrf_token()
    
    # Stub events
    events = [
        {"id": 1, "title": "Car Booking", "date": "2026-01-25", "time": "10:00 AM"},
        {"id": 2, "title": "Health Checkup", "date": "2026-01-30", "time": "2:00 PM"},
    ]
    
    return templates.TemplateResponse(
        "calendar.html",
        {
            "request": request,
            "events": events,
            "csrf_token": csrf_token,
            "page": "calendar"
        }
    )
