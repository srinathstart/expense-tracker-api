from fastapi import FastAPI
from models import Expense, Category, ExpenseCreate
from storage import expenses, save_expenses
import uuid
from datetime import datetime
from fastapi import HTTPException
from database import engine
from models import Base
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import ExpenseCreate, ExpenseResponse
from models import Expense as ExpenseModel
from typing import List
from sqlalchemy import func

Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}

@app.post("/expenses", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = ExpenseModel(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@app.get("/expenses", response_model=List[ExpenseResponse])
def get_expenses(category: str = None, db: Session = Depends(get_db)):
    
    if category:
        expenses = db.query(ExpenseModel).filter(ExpenseModel.category == category).all()
    else:
        expenses = db.query(ExpenseModel).all()

    return expenses

@app.get("/expenses/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: str, db: Session = Depends(get_db)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str, db: Session = Depends(get_db)):
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted"}

@app.put("/expenses/{expense_id}", response_model=ExpenseResponse)
def update_expense(expense_id: str, updated: ExpenseCreate, db: Session = Depends(get_db)):
    
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.amount = updated.amount
    expense.category = updated.category
    expense.note = updated.note

    db.commit()
    db.refresh(expense)

    return expense

@app.get("/summary/{month}")
def get_summary(month: str, db: Session = Depends(get_db)):

    result = db.query(
        ExpenseModel.category,
        func.sum(ExpenseModel.amount)
    ).filter(
        func.to_char(ExpenseModel.date, "YYYY-MM") == month
    ).group_by(ExpenseModel.category).all()

    if not result:
        return {"message": "No expenses found for this month"}

    summary = {category: total for category, total in result}

    return summary
