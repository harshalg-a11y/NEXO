from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/education", tags=["education"])

@router.get("/courses")
def list_courses():
    # TODO: implement education courses retrieval
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Education courses not implemented")
