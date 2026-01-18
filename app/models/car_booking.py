from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class CarBooking(Base):
    __tablename__ = "car_bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False, index=True)
    pickup_location = Column(String(255), nullable=True)
    dropoff_location = Column(String(255), nullable=True)
    pickup_date = Column(DateTime(timezone=True), nullable=False)
    dropoff_date = Column(DateTime(timezone=True), nullable=False)
    total_price = Column(Float, nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="car_bookings")
    car = relationship("Car", back_populates="bookings")