from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from database import engine, get_db
from models import Base, Expense as ExpenseModel
from schemas import ExpenseCreate, ExpenseResponse

from models import User
from schemas import UserCreate, UserResponse
from auth_utils import hash_password

from schemas import UserLogin, TokenRefresh
from auth_utils import verify_password
from auth import create_access_token, create_refresh_token, verify_refresh_token, get_current_user


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}

@app.post("/expenses", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    db_expense = ExpenseModel(**expense.model_dump())
    db_expense.user_id = user_id
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses(category: str = None, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    if category:
        expenses = db.query(ExpenseModel).filter(ExpenseModel.user_id == user_id, ExpenseModel.category == category).all()
    else:
        expenses = db.query(ExpenseModel).filter(ExpenseModel.user_id == user_id).all()
    return expenses

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id, ExpenseModel.user_id == user_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id, ExpenseModel.user_id == user_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted"}

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: str, updated: ExpenseCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id, ExpenseModel.user_id == user_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.amount = updated.amount
    expense.category = updated.category
    expense.note = updated.note

    db.commit()
    db.refresh(expense)

    return expense

@app.get("/summary/{month}")
def get_summary(month: str, db: Session = Depends(get_db), user_id: str = Depends(get_current_user)):
    result = db.query(
        ExpenseModel.category,
        func.sum(ExpenseModel.amount)
    ).filter(
        ExpenseModel.user_id == user_id,
        func.to_char(ExpenseModel.date, "YYYY-MM") == month
    ).group_by(ExpenseModel.category).all()

    if not result:
        return {"message": "No expenses found for this month"}

    summary = {category: total for category, total in result}

    return summary

@app.post("/refresh")
def refresh_token(body: TokenRefresh):
    user_id = verify_refresh_token(body.refresh_token)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    access_token = create_access_token({"user_id": user_id})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    # check if user exists
    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # hash password
    hashed_password = hash_password(user.password)

    # create user
    new_user = User(
        username=user.username,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    # find user
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # verify password
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # create tokens
    access_token = create_access_token({"user_id": db_user.id})
    refresh_token = create_refresh_token({"user_id": db_user.id})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
