# 💸 Expense Tracker API

A clean and minimal **RESTful API** built using FastAPI to manage daily expenses.
This project demonstrates core backend development concepts including CRUD operations, data validation, filtering, aggregation, and persistence.

---

## 🚀 Features

* ✅ Create, read, update, and delete expenses (CRUD)
* 🔍 Filter expenses by category
* 📊 Monthly summary (total spending per category)
* 💾 JSON-based data persistence (no database required)
* ⚡ FastAPI-powered high-performance API
* 🧠 Clean project structure and modular design

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Language:** Python
* **Data Validation:** Pydantic
* **Server:** Uvicorn
* **Storage:** JSON file

---

## 📂 Project Structure

```
Expense-tracker/
│── main.py          # API routes and logic
│── storage.py       # Load & save functions
│── models.py        # Pydantic models
│── expenses.json    # Data storage
│── .gitignore
│── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/expense-tracker-api.git
cd expense-tracker-api
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Install dependencies

```bash
pip install fastapi uvicorn
```

---

### 4. Run the server

```bash
uvicorn main:app --reload
```

---

### 5. Open API docs

```text
http://127.0.0.1:8000/docs
```

---

## 📌 API Endpoints

### ➤ Create Expense

```
POST /expenses
```

---

### ➤ Get All Expenses

```
GET /expenses
```

Optional query:

```
/expenses?category=FOOD
```

---

### ➤ Get Expense by ID

```
GET /expenses/{id}
```

---

### ➤ Update Expense

```
PUT /expenses/{id}
```

---

### ➤ Delete Expense

```
DELETE /expenses/{id}
```

---

### ➤ Monthly Summary

```
GET /summary/{month}
```

Example:

```
/summary/2026-04
```

Response:

```json
{
  "FOOD": 300,
  "TRANSPORT": 50
}
```

---

## 🧠 What I Learned

* Designing REST APIs using FastAPI
* Handling request body, path params, and query params
* Data validation using Pydantic models
* Implementing CRUD operations
* Working with JSON file storage
* Error handling using HTTP status codes
* Writing clean and maintainable backend code

---

## 🔮 Future Improvements

* 🔐 Add authentication (JWT)
* 🗄️ Integrate database (SQLite/PostgreSQL)
* 📈 Add analytics dashboard
* 🌐 Deploy API (Render / Railway)

---

