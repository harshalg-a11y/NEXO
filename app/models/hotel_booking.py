from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class HotelBooking(Base):
    __tablename__ = "hotel_bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    hotel_name = Column(String(255), nullable=False)
    room_type = Column(String(100), nullable=True)
    check_in_date = Column(DateTime(timezone=True), nullable=False)
    check_out_date = Column(DateTime(timezone=True), nullable=False)
    total_price = Column(Float, nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="hotel_bookings")