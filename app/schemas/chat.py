from typing import Optional
from pydantic import BaseModel

class ChatMessage(BaseModel):
    message: str
    model: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    model: str
