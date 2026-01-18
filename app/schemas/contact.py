from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ContactBase(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None

class ContactCreate(ContactBase):
    user_id: int

class ContactUpdate(ContactBase):
    pass

class ContactOut(ContactBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
