from pydantic import BaseModel, field_validator
from datetime import datetime
from models import Category

class ExpenseCreate(BaseModel):
    amount: float
    category: Category
    note: str | None = None

    @field_validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value


class ExpenseResponse(ExpenseCreate):
    id: str
    date: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters")
        return value    

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters")
        if len(value) > 72:
            raise ValueError("Password too long")
        return value


class UserResponse(BaseModel):
    id: str
    username: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class TokenRefresh(BaseModel):
    refresh_token: str

