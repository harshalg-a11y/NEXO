from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.security import require_auth, CSRFProtection, verify_csrf
from app.services.openai_service import openai_service

router = APIRouter(prefix="/agro")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def agro_page(request: Request):
    """Agriculture advice page"""
    user_id = require_auth(request)
    
    csrf_token = CSRFProtection.generate_csrf_token()
    
    # Stub plant data
    plants = [
        {"id": 1, "name": "Tomato", "season": "Summer", "care": "Regular watering"},
        {"id": 2, "name": "Wheat", "season": "Winter", "care": "Moderate watering"},
        {"id": 3, "name": "Rice", "season": "Monsoon", "care": "Plenty of water"},
    ]
    
    return templates.TemplateResponse(
        "agro.html",
        {
            "request": request,
            "plants": plants,
            "csrf_token": csrf_token,
            "page": "agro"
        }
    )


@router.post("/analyze")
async def analyze_plant(
    request: Request,
    plant_description: str = Form(...),
    csrf_token: str = Form(...)
):
    """Analyze plant and get care advice"""
    user_id = require_auth(request)
    verify_csrf(request, csrf_token)
    
    response = await openai_service.analyze_plant(plant_description)
    
    return JSONResponse({
        "status": "success",
        "response": response
    })
