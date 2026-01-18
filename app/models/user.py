from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), nullable=False, default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    contacts = relationship("Contact", back_populates="user", cascade="all, delete-orphan")
    car_bookings = relationship("CarBooking", back_populates="user", cascade="all, delete-orphan")
    hotel_bookings = relationship("HotelBooking", back_populates="user", cascade="all, delete-orphan")
    transactions = relationship("NexoPaisaTransaction", back_populates="user", cascade="all, delete-orphan")