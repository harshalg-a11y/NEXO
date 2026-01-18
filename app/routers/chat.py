from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.security import require_auth, CSRFProtection, verify_csrf
from app.services.openai_service import openai_service

router = APIRouter(prefix="/chat")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def chat_page(request: Request):
    """AI chat page"""
    user_id = require_auth(request)
    
    csrf_token = CSRFProtection.generate_csrf_token()
    
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "csrf_token": csrf_token,
            "page": "chat"
        }
    )


@router.post("/message")
async def send_message(
    request: Request,
    message: str = Form(...),
    csrf_token: str = Form(...)
):
    """Send chat message to AI"""
    user_id = require_auth(request)
    verify_csrf(request, csrf_token)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant for the NEXO platform."},
        {"role": "user", "content": message}
    ]
    
    response = await openai_service.chat_completion(messages)
    
    return JSONResponse({
        "status": "success",
        "response": response
    })
