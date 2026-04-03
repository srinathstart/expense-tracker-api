from pydantic import BaseModel
from enum import Enum
from datetime import datetime

class Category(str, Enum):
    FOOD = "FOOD"
    TRANSPORT = "TRANSPORT"
    BILLS = "BILLS"
    ENTERTAINMENT = "ENTERTAINMENT"

class Expense(BaseModel):
    id: str
    amount: float
    category: Category
    note: str | None = None
    date: datetime

class ExpenseCreate(BaseModel):
    amount: float
    category: Category
    note: str | None = None

