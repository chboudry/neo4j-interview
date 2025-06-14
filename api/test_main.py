"""
Test file for the Neo4j Interview API
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from routes import routes

client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Neo4j Interview API"}


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_employees_endpoint():
    """Test the employees endpoint"""
    response = client.get("/employees")
    assert response.status_code == 200
    data = response.json()
    assert "employees" in data
    assert "total" in data
    assert isinstance(data["employees"], list)
    assert isinstance(data["total"], int)
