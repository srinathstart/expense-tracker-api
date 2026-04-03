from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid


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

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    note = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

