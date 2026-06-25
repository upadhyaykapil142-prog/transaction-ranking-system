from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True, index=True)
    total_points = Column(Float, default=0)
    transaction_count = Column(Integer, default=0)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, index=True)
    amount = Column(Float)
    request_id = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)