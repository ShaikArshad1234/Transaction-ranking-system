from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from database import SessionLocal
from database import engine

from models import Base
from models import Transaction

from schemas import TransactionRequest

from services import calculate_ranking

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "API Running"}


@app.post("/transaction")
def create_transaction(
    payload: TransactionRequest,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(Transaction)
        .filter(
            Transaction.transaction_id
            == payload.transactionId
        )
        .first()
    )

    if existing:

        raise HTTPException(
            status_code=409,
            detail="Duplicate transaction"
        )

    txn = Transaction(
        transaction_id=payload.transactionId,
        user_id=payload.userId,
        amount=payload.amount
    )

    db.add(txn)

    db.commit()

    return {
        "message": "Transaction Created"
    }


@app.get("/summary/{user_id}")
def summary(
    user_id: str,
    db: Session = Depends(get_db)
):

    txns = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == user_id
        )
        .all()
    )

    if not txns:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    total = sum(
        t.amount
        for t in txns
    )

    return {
        "userId": user_id,
        "transactionCount": len(txns),
        "totalAmount": total
    }


@app.get("/ranking")
def ranking(
    db: Session = Depends(get_db)
):

    return calculate_ranking(db)