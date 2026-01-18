from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message")
def send_message():
    # TODO: implement chat message handling
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Chat not implemented")
