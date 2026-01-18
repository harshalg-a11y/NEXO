from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from app.models.user import User
from app.security import get_current_user

router = APIRouter(prefix="/calendar", tags=["calendar"])

@router.get("/events")
def list_events(current_user: User = Depends(get_current_user)):
    """List upcoming calendar events"""
    now = datetime.utcnow()
    return {
        "events": [
            {
                "id": 1,
                "title": "Doctor Appointment",
                "description": "General checkup at NEXO Health Center",
                "start_time": (now + timedelta(days=2)).isoformat(),
                "end_time": (now + timedelta(days=2, hours=1)).isoformat(),
                "category": "health",
                "location": "NEXO Health Center"
            },
            {
                "id": 2,
                "title": "Digital Literacy Class",
                "description": "Week 1: Computer Basics",
                "start_time": (now + timedelta(days=5)).isoformat(),
                "end_time": (now + timedelta(days=5, hours=2)).isoformat(),
                "category": "education",
                "location": "Online"
            }
        ]
    }

@router.get("/events/{event_id}")
def get_event(event_id: int, current_user: User = Depends(get_current_user)):
    """Get details of a specific event"""
    now = datetime.utcnow()
    return {
        "id": event_id,
        "title": "Sample Event",
        "description": "Event details",
        "start_time": (now + timedelta(days=1)).isoformat(),
        "end_time": (now + timedelta(days=1, hours=1)).isoformat(),
        "category": "general",
        "location": "TBD",
        "reminders": [
            {"time": "1 day before", "sent": False},
            {"time": "1 hour before", "sent": False}
        ]
    }

@router.get("/upcoming")
def get_upcoming_events(current_user: User = Depends(get_current_user)):
    """Get events in the next 7 days"""
    now = datetime.utcnow()
    return {
        "events": [
            {
                "id": 1,
                "title": "Doctor Appointment",
                "start_time": (now + timedelta(days=2)).isoformat(),
                "category": "health"
            }
        ],
        "count": 1,
        "period": "next 7 days"
    }
