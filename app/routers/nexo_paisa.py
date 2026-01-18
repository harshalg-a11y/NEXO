from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.models.nexo_paisa_transaction import NexoPaisaTransaction
from app.security import get_current_user
from app.schemas.nexo_paisa import (
    NexoPaisaPaymentRequest,
    NexoPaisaPaymentResponse,
    NexoPaisaWebhookPayload,
    NexoPaisaTransactionOut
)
from app.services.nexo_paisa_service import nexo_paisa_service

router = APIRouter(prefix="/nexo-paisa", tags=["nexo-paisa"])

@router.post("/pay", response_model=NexoPaisaPaymentResponse)
def initiate_payment(
    payload: NexoPaisaPaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initiate a Nexo Paisa payment"""
    # Create transaction record
    transaction = NexoPaisaTransaction(
        user_id=current_user.id,
        amount=payload.amount,
        currency=payload.currency,
        description=payload.description,
        status="pending"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    # Create payment with Nexo Paisa service
    payment_result = nexo_paisa_service.create_payment(
        amount=payload.amount,
        currency=payload.currency,
        description=payload.description,
        return_url=payload.return_url
    )
    
    # Update transaction with reference
    if payment_result.get("success"):
        transaction.reference = payment_result.get("reference")
        db.commit()
    
    return NexoPaisaPaymentResponse(
        transaction_id=transaction.id,
        payment_url=payment_result.get("payment_url"),
        status=transaction.status,
        message=payment_result.get("message", "Payment initiated")
    )

@router.post("/webhook")
def webhook_handler(payload: NexoPaisaWebhookPayload, db: Session = Depends(get_db)):
    """Handle Nexo Paisa webhook callbacks"""
    # Verify signature if provided
    if payload.signature:
        is_valid = nexo_paisa_service.verify_webhook_signature(
            payload.dict(), 
            payload.signature
        )
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid webhook signature"
            )
    
    # Find transaction
    transaction = db.query(NexoPaisaTransaction).filter(
        NexoPaisaTransaction.id == payload.transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Update transaction status
    transaction.status = payload.status
    transaction.reference = payload.reference
    db.commit()
    
    return {"success": True, "message": "Webhook processed"}

@router.get("/transactions/{transaction_id}", response_model=NexoPaisaTransactionOut)
def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific transaction"""
    transaction = db.query(NexoPaisaTransaction).filter(
        NexoPaisaTransaction.id == transaction_id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Users can only view their own transactions unless admin
    if transaction.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this transaction"
        )
    
    return transaction
