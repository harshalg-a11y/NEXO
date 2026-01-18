from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.car import Car
from app.models.booking import CarBooking, HotelBooking
from app.security import require_auth, CSRFProtection, verify_csrf

router = APIRouter(prefix="/travel")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def travel_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """Travel booking page"""
    user_id = require_auth(request)
    
    # Get available cars
    cars = db.query(Car).filter(Car.is_available == True).limit(10).all()
    
    csrf_token = CSRFProtection.generate_csrf_token()
    
    return templates.TemplateResponse(
        "travel.html",
        {
            "request": request,
            "cars": cars,
            "csrf_token": csrf_token,
            "page": "travel"
        }
    )


@router.post("/book-car")
async def book_car(
    request: Request,
    car_id: int = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db)
):
    """Book a car"""
    user_id = require_auth(request)
    verify_csrf(request, csrf_token)
    
    # Stub: Create booking logic here
    booking = CarBooking(
        user_id=user_id,
        car_id=car_id,
        start_date=start_date,
        end_date=end_date,
        total_price=0  # Calculate based on dates and car price
    )
    db.add(booking)
    db.commit()
    
    return JSONResponse({"status": "success", "message": "Car booking created"})


@router.post("/book-hotel")
async def book_hotel(
    request: Request,
    hotel_name: str = Form(...),
    location: str = Form(...),
    check_in: str = Form(...),
    check_out: str = Form(...),
    guests: int = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db)
):
    """Book a hotel"""
    user_id = require_auth(request)
    verify_csrf(request, csrf_token)
    
    # Stub: Create hotel booking logic here
    booking = HotelBooking(
        user_id=user_id,
        hotel_name=hotel_name,
        location=location,
        check_in_date=check_in,
        check_out_date=check_out,
        num_guests=guests,
        total_price=0  # Calculate based on dates and hotel pricing
    )
    db.add(booking)
    db.commit()
    
    return JSONResponse({"status": "success", "message": "Hotel booking created"})
