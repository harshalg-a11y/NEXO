from fastapi import APIRouter, Depends
from app.models.user import User
from app.security import get_current_user

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/status")
def health_status(current_user: User = Depends(get_current_user)):
    """Get health services and clinic information"""
    return {
        "services": [
            {
                "id": 1,
                "name": "General Consultation",
                "description": "Consultation with general practitioners",
                "price": 500.0,
                "currency": "NPR"
            },
            {
                "id": 2,
                "name": "Dental Care",
                "description": "Dental checkup and treatment",
                "price": 1000.0,
                "currency": "NPR"
            },
            {
                "id": 3,
                "name": "Laboratory Tests",
                "description": "Blood tests, urine tests, and more",
                "price": 800.0,
                "currency": "NPR"
            }
        ],
        "clinics": [
            {
                "name": "NEXO Health Center",
                "address": "Kathmandu, Nepal",
                "phone": "+977-1-4444444",
                "services": ["General", "Dental", "Laboratory"]
            }
        ]
    }

@router.get("/appointments")
def list_appointments(current_user: User = Depends(get_current_user)):
    """List user's health appointments"""
    return {
        "appointments": [
            {
                "id": 1,
                "service": "General Consultation",
                "clinic": "NEXO Health Center",
                "date": "2024-02-15T10:00:00",
                "status": "scheduled"
            }
        ],
        "message": "Appointment booking feature coming soon"
    }

@router.get("/records")
def get_health_records(current_user: User = Depends(get_current_user)):
    """Get user's health records"""
    return {
        "records": [],
        "message": "Health records feature in development"
    }
