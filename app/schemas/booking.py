from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BookingBase(BaseModel):
    pass

class CarBookingOut(BaseModel):
    id: int
    user_id: int
    car_id: int
    pickup_location: Optional[str] = None
    dropoff_location: Optional[str] = None
    pickup_date: datetime
    dropoff_date: datetime
    total_price: Optional[float] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class HotelBookingOut(BaseModel):
    id: int
    user_id: int
    hotel_name: str
    room_type: Optional[str] = None
    check_in_date: datetime
    check_out_date: datetime
    total_price: Optional[float] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
