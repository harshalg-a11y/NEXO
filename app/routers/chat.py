from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import User
from app.security import get_current_user
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.openai_service import generate_response

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message", response_model=ChatResponse)
def send_message(
    payload: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """Send a message to the AI chat assistant"""
    try:
        response_text = generate_response(
            prompt=payload.message,
            model=payload.model
        )
        
        return ChatResponse(
            response=response_text,
            model=payload.model or "gpt-3.5-turbo"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )
