from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/nexo-paisa", tags=["nexo-paisa"])

@router.post("/pay")
def pay():
    # TODO: implement Nexo Paisa payment integration
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Nexo Paisa payment not implemented")
