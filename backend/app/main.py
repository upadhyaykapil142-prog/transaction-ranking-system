from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .models import User, Transaction
from .schemas import TransactionCreate

app = FastAPI(title="Transaction Ranking API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "message": "Transaction Ranking API Running"
    }


@app.post("/transaction")
def create_transaction(payload: TransactionCreate):

    db: Session = SessionLocal()

    try:
        existing = (
            db.query(Transaction)
            .filter(Transaction.request_id == payload.requestId)
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Duplicate request"
            )

        transaction = Transaction(
            user_id=payload.userId,
            amount=payload.amount,
            request_id=payload.requestId
        )

        db.add(transaction)

        user = (
            db.query(User)
            .filter(User.user_id == payload.userId)
            .first()
        )

        if not user:
            user = User(
                user_id=payload.userId,
                total_points=0,
                transaction_count=0
            )
            db.add(user)

        user.total_points += payload.amount
        user.transaction_count += 1

        db.commit()

        return {
            "success": True,
            "userId": payload.userId,
            "amount": payload.amount
        }

    finally:
        db.close()


@app.get("/summary/{user_id}")
def get_summary(user_id: str):

    db: Session = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "userId": user.user_id,
            "totalPoints": user.total_points,
            "transactionCount": user.transaction_count
        }

    finally:
        db.close()


@app.get("/ranking")
def get_ranking():

    db: Session = SessionLocal()

    try:
        users = db.query(User).all()

        ranking = []

        for user in users:

            score = (
                user.total_points * 0.7
                + user.transaction_count * 10
            )

            ranking.append({
                "userId": user.user_id,
                "totalPoints": user.total_points,
                "transactionCount": user.transaction_count,
                "score": round(score, 2)
            })

        ranking.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return ranking

    finally:
        db.close()