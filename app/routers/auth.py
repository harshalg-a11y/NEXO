from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.auth import UserCreate, UserLogin, UserOut, Token
from app.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    # TODO: implement real user creation, hashing, and persistence
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Registration not implemented")

@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    # TODO: implement real authentication and token issuance
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Login not implemented")

@router.get("/me", response_model=UserOut)
def me(db: Session = Depends(get_db)):
    # TODO: implement current user retrieval
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Current user endpoint not implemented")
