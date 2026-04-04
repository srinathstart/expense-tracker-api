from enum import Enum
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import uuid


class Category(str, Enum):
    FOOD = "FOOD"
    TRANSPORT = "TRANSPORT"
    BILLS = "BILLS"
    ENTERTAINMENT = "ENTERTAINMENT"

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    note = Column(String)
    user_id = Column(String, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
