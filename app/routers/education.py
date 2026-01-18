from fastapi import APIRouter, Depends
from app.models.user import User
from app.security import get_current_user

router = APIRouter(prefix="/education", tags=["education"])

@router.get("/courses")
def list_courses(current_user: User = Depends(get_current_user)):
    """List available educational courses"""
    return {
        "courses": [
            {
                "id": 1,
                "title": "Digital Literacy Basics",
                "description": "Learn essential computer and internet skills",
                "category": "Technology",
                "duration_weeks": 4,
                "price": 5000.0,
                "currency": "NPR",
                "level": "Beginner"
            },
            {
                "id": 2,
                "title": "English Language Course",
                "description": "Improve your English communication skills",
                "category": "Language",
                "duration_weeks": 12,
                "price": 8000.0,
                "currency": "NPR",
                "level": "All Levels"
            },
            {
                "id": 3,
                "title": "Basic Accounting",
                "description": "Learn fundamental accounting principles",
                "category": "Business",
                "duration_weeks": 6,
                "price": 6000.0,
                "currency": "NPR",
                "level": "Beginner"
            }
        ]
    }

@router.get("/courses/{course_id}")
def get_course_details(course_id: int, current_user: User = Depends(get_current_user)):
    """Get detailed information about a specific course"""
    # Mock course details
    return {
        "id": course_id,
        "title": "Digital Literacy Basics",
        "description": "Comprehensive course on computer and internet skills",
        "category": "Technology",
        "duration_weeks": 4,
        "price": 5000.0,
        "currency": "NPR",
        "level": "Beginner",
        "syllabus": [
            {"week": 1, "topic": "Computer Basics and Operating Systems"},
            {"week": 2, "topic": "Internet and Email Usage"},
            {"week": 3, "topic": "Document Creation and Editing"},
            {"week": 4, "topic": "Online Safety and Security"}
        ],
        "instructor": "Expert Instructor",
        "enrolled_students": 45
    }

@router.get("/enrollments")
def list_enrollments(current_user: User = Depends(get_current_user)):
    """List courses the user is enrolled in"""
    return {
        "enrollments": [],
        "message": "No current enrollments. Browse courses to get started!"
    }

@router.get("/resources")
def list_resources(current_user: User = Depends(get_current_user)):
    """List educational resources and materials"""
    return {
        "resources": [
            {
                "id": 1,
                "title": "Free Digital Skills Tutorial",
                "type": "video",
                "url": "https://example.com/tutorial1"
            },
            {
                "id": 2,
                "title": "English Grammar Guide",
                "type": "pdf",
                "url": "https://example.com/guide.pdf"
            }
        ]
    }
