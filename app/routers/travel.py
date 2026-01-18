from typing import List
from fastapi import APIRouter, Depends
from app.models.user import User
from app.security import get_current_user

router = APIRouter(prefix="/travel", tags=["travel"])

@router.get("/packages")
def list_packages(current_user: User = Depends(get_current_user)):
    """List available travel packages"""
    return {
        "packages": [
            {
                "id": 1,
                "name": "Kathmandu Heritage Tour",
                "description": "Explore the rich cultural heritage of Kathmandu Valley",
                "duration_days": 3,
                "price": 15000.0,
                "currency": "NPR",
                "destinations": ["Kathmandu", "Bhaktapur", "Patan"]
            },
            {
                "id": 2,
                "name": "Pokhara Adventure",
                "description": "Experience paragliding, boating, and mountain views",
                "duration_days": 4,
                "price": 25000.0,
                "currency": "NPR",
                "destinations": ["Pokhara", "Sarangkot"]
            },
            {
                "id": 3,
                "name": "Chitwan Wildlife Safari",
                "description": "Discover Nepal's wildlife in Chitwan National Park",
                "duration_days": 2,
                "price": 18000.0,
                "currency": "NPR",
                "destinations": ["Chitwan"]
            }
        ]
    }

@router.get("/packages/{package_id}")
def get_package(package_id: int, current_user: User = Depends(get_current_user)):
    """Get details of a specific travel package"""
    # Mock package details
    packages = {
        1: {
            "id": 1,
            "name": "Kathmandu Heritage Tour",
            "description": "Explore the rich cultural heritage of Kathmandu Valley including UNESCO World Heritage Sites",
            "duration_days": 3,
            "price": 15000.0,
            "currency": "NPR",
            "destinations": ["Kathmandu", "Bhaktapur", "Patan"],
            "included": ["Accommodation", "Breakfast", "Guided tours", "Entry fees"],
            "itinerary": [
                {"day": 1, "activities": "Arrival and Kathmandu Durbar Square visit"},
                {"day": 2, "activities": "Swayambhunath, Pashupatinath, and Boudhanath"},
                {"day": 3, "activities": "Bhaktapur and Patan exploration"}
            ]
        }
    }
    
    package = packages.get(package_id, {
        "id": package_id,
        "name": f"Package {package_id}",
        "description": "Package details coming soon",
        "duration_days": 3,
        "price": 20000.0,
        "currency": "NPR"
    })
    
    return package

@router.get("/destinations")
def list_destinations(current_user: User = Depends(get_current_user)):
    """List popular travel destinations"""
    return {
        "destinations": [
            {"name": "Kathmandu", "description": "Capital city with rich cultural heritage"},
            {"name": "Pokhara", "description": "Gateway to Himalayas with stunning lake views"},
            {"name": "Chitwan", "description": "Wildlife and nature paradise"},
            {"name": "Lumbini", "description": "Birthplace of Lord Buddha"},
            {"name": "Everest Base Camp", "description": "Trek to the base of world's highest peak"}
        ]
    }
