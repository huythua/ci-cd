import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data

def test_get_info():
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "DevOps CI/CD Service is running successfully!"
    assert data["data"]["app_name"] == "devops-backend-api"

def test_calculate_add():
    response = client.get("/api/v1/calculate?a=10&b=5&op=add")
    assert response.status_code == 200
    assert response.json() == {"result": 15.0}

def test_calculate_divide_by_zero():
    response = client.get("/api/v1/calculate?a=10&b=0&op=divide")
    assert response.status_code == 400
    assert "Cannot divide by zero" in response.json()["detail"]
