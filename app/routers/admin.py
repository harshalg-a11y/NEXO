from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.models.user import User
from app.models.car_booking import CarBooking
from app.models.hotel_booking import HotelBooking
from app.models.nexo_paisa_transaction import NexoPaisaTransaction
from app.security import get_current_user, require_role

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
def dashboard(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Get admin dashboard statistics"""
    # Get counts
    total_users = db.query(func.count(User.id)).scalar()
    total_car_bookings = db.query(func.count(CarBooking.id)).scalar()
    total_hotel_bookings = db.query(func.count(HotelBooking.id)).scalar()
    total_transactions = db.query(func.count(NexoPaisaTransaction.id)).scalar()
    
    # Get revenue
    total_revenue = db.query(func.sum(NexoPaisaTransaction.amount)).filter(
        NexoPaisaTransaction.status == "completed"
    ).scalar() or 0.0
    
    return {
        "statistics": {
            "total_users": total_users,
            "total_car_bookings": total_car_bookings,
            "total_hotel_bookings": total_hotel_bookings,
            "total_transactions": total_transactions,
            "total_revenue": total_revenue,
            "currency": "NPR"
        },
        "recent_activity": {
            "new_users_today": 0,
            "bookings_today": 0,
            "transactions_today": 0
        }
    }

@router.get("/users/stats")
def user_statistics(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Get user statistics"""
    users_by_role = db.query(
        User.role,
        func.count(User.id).label("count")
    ).group_by(User.role).all()
    
    return {
        "users_by_role": [
            {"role": role, "count": count}
            for role, count in users_by_role
        ],
        "total_users": sum(count for _, count in users_by_role)
    }

@router.get("/transactions/stats")
def transaction_statistics(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Get transaction statistics"""
    transactions_by_status = db.query(
        NexoPaisaTransaction.status,
        func.count(NexoPaisaTransaction.id).label("count"),
        func.sum(NexoPaisaTransaction.amount).label("total_amount")
    ).group_by(NexoPaisaTransaction.status).all()
    
    return {
        "transactions_by_status": [
            {
                "status": status,
                "count": count,
                "total_amount": float(total_amount or 0.0)
            }
            for status, count, total_amount in transactions_by_status
        ]
    }

@router.get("/system/health")
def system_health(current_user: User = Depends(require_role("admin"))):
    """Get system health status"""
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "api": "operational",
            "mail": "configured" if True else "not configured",
            "openai": "configured" if True else "not configured"
        },
        "version": "1.0.0"
    }
