from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/travel", tags=["travel"])

@router.get("/packages")
def list_packages():
    # TODO: implement travel packages retrieval
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Travel packages not implemented")
