import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Expense Tracker API is running"}


def test_register():
    response = client.post("/register", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code in (200, 400)


def test_register_short_password():
    response = client.post("/register", json={
        "username": "testuser2",
        "password": "123"
    })
    assert response.status_code == 422


def test_login_wrong_password():
    response = client.post("/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 400


def test_get_expenses_without_token():
    response = client.get("/expenses")
    assert response.status_code == 401


def test_create_expense_without_token():
    response = client.post("/expenses", json={
        "amount": 100,
        "category": "FOOD",
        "note": "lunch"
    })
    assert response.status_code == 401


def test_refresh_invalid_token():
    response = client.post("/refresh", json={"refresh_token": "invalidtoken"})
    assert response.status_code == 401
