from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    userId: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    requestId: str = Field(..., min_length=1)