from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/dashboard")
def dashboard():
    # TODO: implement admin dashboard data
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Admin dashboard not implemented")
