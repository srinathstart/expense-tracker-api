from fastapi import FastAPI
from models import Expense, Category, ExpenseCreate
from storage import expenses, save_expenses
import uuid
from datetime import datetime
from fastapi import HTTPException


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running"}

@app.post("/expenses")
def create_expense(expense: ExpenseCreate):
    new_expense = Expense(
    id = str(uuid.uuid4()),
    amount = expense.amount,
    category = expense.category,
    note = expense.note,
    date = datetime.now()
    )
    expenses.append(new_expense)
    save_expenses([e.dict() for e in expenses])
    return new_expense

@app.get("/expenses")
def get_expenses(category: Category = None):
    if category:
        return [exp for exp in expenses if exp.category == category]
    return expenses

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: str):
    for exp in expenses:
        if exp.id == expense_id:
            return exp
    raise HTTPException(status_code=404, detail="Expense not found")

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: str):
    for i, exp in enumerate(expenses):
        if exp.id == expense_id:
            expenses.pop(i)
            save_expenses([e.dict() for e in expenses])
            return {"message": "Expense deleted"}
    raise HTTPException(status_code=404, detail="Expense not found")

@app.put("/expenses/{expense_id}")
def update_expense(expense_id: str, updated_data: ExpenseCreate):
    for exp in expenses:
        if exp.id == expense_id:
            exp.amount = updated_data.amount
            exp.category = updated_data.category
            exp.note = updated_data.note
            save_expenses([e.dict() for e in expenses])
            return exp 
    raise HTTPException(status_code=404, detail="Expense not found")

@app.get("/summary/{month}")
def get_summary(month: str):
    summary = {}

    for exp in expenses:
        if exp.date.strftime("%Y-%m").startswith(month):
            cat = exp.category.value

            if cat in summary:
                summary[cat] += exp.amount
            else:
                summary[cat] = exp.amount
        
    if not summary:
        return {"message": "No expenses found for this month"}

    return summary
