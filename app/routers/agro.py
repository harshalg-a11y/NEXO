from fastapi import APIRouter, Depends
from app.models.user import User
from app.security import get_current_user

router = APIRouter(prefix="/agro", tags=["agro"])

@router.get("/advice")
def get_agro_advice(current_user: User = Depends(get_current_user)):
    """Get agricultural advice and tips"""
    return {
        "tips": [
            {
                "id": 1,
                "category": "Crop Management",
                "title": "Rice Cultivation Tips",
                "content": "Ensure proper water management and timely fertilizer application for better yield"
            },
            {
                "id": 2,
                "category": "Pest Control",
                "title": "Natural Pest Management",
                "content": "Use neem oil and companion planting to control pests naturally"
            },
            {
                "id": 3,
                "category": "Soil Health",
                "title": "Composting Guide",
                "content": "Create nutrient-rich compost using kitchen waste and farm residues"
            }
        ],
        "weather": {
            "location": "Kathmandu",
            "temperature": "24°C",
            "condition": "Partly cloudy",
            "forecast": "Good conditions for planting"
        }
    }

@router.get("/markets")
def get_market_prices(current_user: User = Depends(get_current_user)):
    """Get current agricultural market prices"""
    return {
        "prices": [
            {"product": "Rice", "price": 45.0, "unit": "kg", "currency": "NPR"},
            {"product": "Wheat", "price": 35.0, "unit": "kg", "currency": "NPR"},
            {"product": "Tomato", "price": 60.0, "unit": "kg", "currency": "NPR"},
            {"product": "Potato", "price": 40.0, "unit": "kg", "currency": "NPR"}
        ],
        "last_updated": "2024-02-10T10:00:00",
        "market": "Kalimati Fruit and Vegetable Market"
    }

@router.get("/equipment")
def list_equipment(current_user: User = Depends(get_current_user)):
    """List available agricultural equipment for rent or purchase"""
    return {
        "equipment": [
            {
                "id": 1,
                "name": "Tractor",
                "type": "rental",
                "price_per_day": 3000.0,
                "currency": "NPR",
                "available": True
            },
            {
                "id": 2,
                "name": "Harvester",
                "type": "rental",
                "price_per_day": 5000.0,
                "currency": "NPR",
                "available": True
            }
        ]
    }
