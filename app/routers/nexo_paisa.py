from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uuid
from app.database import get_db
from app.models.nexo_paisa import NexoPaisaTransaction, TransactionType, TransactionStatus
from app.security import require_auth, CSRFProtection, verify_csrf

router = APIRouter(prefix="/nexo-paisa")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
async def nexo_paisa_page(
    request: Request,
    db: Session = Depends(get_db)
):
    """Nexo Paisa wallet page"""
    user_id = require_auth(request)
    
    # Get user's transactions
    transactions = db.query(NexoPaisaTransaction)\
        .filter(NexoPaisaTransaction.user_id == user_id)\
        .order_by(NexoPaisaTransaction.created_at.desc())\
        .limit(20)\
        .all()
    
    # Calculate balance (stub)
    balance = 0
    for txn in transactions:
        if txn.balance_after:
            balance = float(txn.balance_after)
            break
    
    csrf_token = CSRFProtection.generate_csrf_token()
    
    return templates.TemplateResponse(
        "load_nexo_paisa.html",
        {
            "request": request,
            "balance": balance,
            "transactions": transactions,
            "csrf_token": csrf_token,
            "page": "nexo-paisa"
        }
    )


@router.post("/load")
async def load_money(
    request: Request,
    amount: float = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db)
):
    """Load money into Nexo Paisa wallet"""
    user_id = require_auth(request)
    verify_csrf(request, csrf_token)
    
    # Get current balance
    last_txn = db.query(NexoPaisaTransaction)\
        .filter(NexoPaisaTransaction.user_id == user_id)\
        .order_by(NexoPaisaTransaction.created_at.desc())\
        .first()
    
    balance_before = float(last_txn.balance_after) if last_txn and last_txn.balance_after else 0
    balance_after = balance_before + amount
    
    # Create transaction
    transaction = NexoPaisaTransaction(
        user_id=user_id,
        transaction_type=TransactionType.DEPOSIT,
        amount=amount,
        balance_before=balance_before,
        balance_after=balance_after,
        status=TransactionStatus.COMPLETED,
        reference_id=str(uuid.uuid4())[:8],
        description="Money loaded to wallet"
    )
    db.add(transaction)
    db.commit()
    
    return JSONResponse({
        "status": "success",
        "message": f"₹{amount} loaded successfully",
        "balance": balance_after
    })


@router.post("/transfer")
async def transfer_money(
    request: Request,
    recipient_email: str = Form(...),
    amount: float = Form(...),
    csrf_token: str = Form(...),
    db: Session = Depends(get_db)
):
    """Transfer money to another user"""
    user_id = require_auth(request)
    verify_csrf(request, csrf_token)
    
    # Stub: Implement transfer logic
    return JSONResponse({
        "status": "success",
        "message": f"₹{amount} transferred to {recipient_email}"
    })
