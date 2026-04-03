import json
from models import Expense

def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            data = json.load(file)
            return [Expense(**item) for item in data]
    except:
        return []
    
def save_expenses(expenses):
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, default=str)

expenses = load_expenses()