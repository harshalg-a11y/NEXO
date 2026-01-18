from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/agro", tags=["agro"])

@router.get("/advice")
def get_agro_advice():
    # TODO: implement agro advice retrieval
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Agro advice not implemented")
