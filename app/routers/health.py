from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/status")
def health_status():
    # TODO: implement health services status
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Health status not implemented")
