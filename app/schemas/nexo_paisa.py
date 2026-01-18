from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class NexoPaisaTransactionCreate(BaseModel):
    amount: float
    currency: str = "NPR"
    description: Optional[str] = None

class NexoPaisaTransactionOut(BaseModel):
    id: int
    user_id: int
    amount: float
    currency: str
    status: str
    reference: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class NexoPaisaPaymentRequest(BaseModel):
    amount: float
    currency: str = "NPR"
    description: Optional[str] = None
    return_url: Optional[str] = None

class NexoPaisaPaymentResponse(BaseModel):
    transaction_id: int
    payment_url: Optional[str] = None
    status: str
    message: str

class NexoPaisaWebhookPayload(BaseModel):
    transaction_id: int
    status: str
    reference: str
    signature: Optional[str] = None
