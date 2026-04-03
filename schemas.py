from pydantic import BaseModel
from datetime import datetime

class ExpenseCreate(BaseModel):
    amount: float
    category: str
    note: str | None = None


class ExpenseResponse(ExpenseCreate):
    id: str
    date: datetime

    class Config:
        from_attributes = True