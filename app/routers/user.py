from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.schemas.user import UserInDB, UserUpdate
from app.schemas.contact import ContactOut
from app.schemas.booking import CarBookingOut, HotelBookingOut
from app.schemas.nexo_paisa import NexoPaisaTransactionOut
from app.security import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserInDB])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """List all users (admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/me", response_model=UserInDB)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile"""
    return current_user

@router.put("/me", response_model=UserInDB)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    if user_update.email is not None:
        # Check if email is already taken
        existing_user = db.query(User).filter(
            User.email == user_update.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        current_user.email = user_update.email
    
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/{user_id}", response_model=UserInDB)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific user by ID"""
    # Users can only view their own profile unless they're admin
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this user"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/{user_id}/contacts", response_model=List[ContactOut])
def get_user_contacts(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get contacts for a specific user"""
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these contacts"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.contacts

@router.get("/{user_id}/bookings/cars", response_model=List[CarBookingOut])
def get_user_car_bookings(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get car bookings for a specific user"""
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these bookings"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.car_bookings

@router.get("/{user_id}/bookings/hotels", response_model=List[HotelBookingOut])
def get_user_hotel_bookings(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get hotel bookings for a specific user"""
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these bookings"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.hotel_bookings

@router.get("/{user_id}/transactions", response_model=List[NexoPaisaTransactionOut])
def get_user_transactions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get Nexo Paisa transactions for a specific user"""
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these transactions"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user.transactions
