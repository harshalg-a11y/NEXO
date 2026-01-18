from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.security import require_auth, CSRFProtection, verify_csrf
from app.services.openai_service import openai_service

router = APIRouter(prefix="/health")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def health_page(request: Request):
    """Health consultation page"""
    user_id = require_auth(request)
    
    csrf_token = CSRFProtection.generate_csrf_token()
    
    return templates.TemplateResponse(
        "health.html",
        {
            "request": request,
            "csrf_token": csrf_token,
            "page": "health"
        }
    )


@router.post("/consult")
async def health_consult(
    request: Request,
    symptoms: str = Form(...),
    csrf_token: str = Form(...)
):
    """Get health consultation"""
    user_id = require_auth(request)
    verify_csrf(request, csrf_token)
    
    response = await openai_service.health_consultation(symptoms)
    
    return JSONResponse({
        "status": "success",
        "response": response
    })
