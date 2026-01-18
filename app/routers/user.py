from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.get("")
def list_users(db: Session = Depends(get_db)):
    # TODO: implement user listing
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="User listing not implemented")

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    # TODO: implement user retrieval
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="User retrieval not implemented")
