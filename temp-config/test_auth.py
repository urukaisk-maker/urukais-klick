"""
Tests para autenticación
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    """Test de login exitoso"""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "test123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    """Test de login con credenciales inválidas"""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_register_success():
    """Test de registro exitoso"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "alias": "testuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_anonymous_login():
    """Test de login anónimo"""
    response = client.post("/api/v1/auth/anonymous")
    assert response.status_code == 200
    assert "access_token" in response.json()
