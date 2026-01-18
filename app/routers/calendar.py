from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/calendar", tags=["calendar"])

@router.get("/events")
def list_events():
    # TODO: implement calendar events retrieval
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Calendar events not implemented")
