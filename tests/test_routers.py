"""Tests for router endpoints"""
import pytest


def test_health_check(client):
    """Test API health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_user_list_as_admin(client, admin_auth_headers, test_user):
    """Test listing users as admin"""
    response = client.get("/users", headers=admin_auth_headers)
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 2  # test_user and admin_user


def test_user_list_as_regular_user(client, auth_headers):
    """Test listing users as regular user fails"""
    response = client.get("/users", headers=auth_headers)
    assert response.status_code == 403


def test_get_current_user_profile(client, auth_headers):
    """Test getting current user's profile"""
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


def test_travel_packages(client, auth_headers):
    """Test getting travel packages"""
    response = client.get("/travel/packages", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "packages" in data
    assert isinstance(data["packages"], list)


def test_health_status(client, auth_headers):
    """Test getting health services status"""
    response = client.get("/health/status", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "services" in data


def test_agro_advice(client, auth_headers):
    """Test getting agro advice"""
    response = client.get("/agro/advice", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "tips" in data


def test_education_courses(client, auth_headers):
    """Test listing education courses"""
    response = client.get("/education/courses", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "courses" in data


def test_calendar_events(client, auth_headers):
    """Test listing calendar events"""
    response = client.get("/calendar/events", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "events" in data


def test_admin_dashboard(client, admin_auth_headers):
    """Test admin dashboard"""
    response = client.get("/admin/dashboard", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "statistics" in data


def test_admin_dashboard_unauthorized(client, auth_headers):
    """Test admin dashboard as regular user fails"""
    response = client.get("/admin/dashboard", headers=auth_headers)
    assert response.status_code == 403


def test_chat_message(client, auth_headers):
    """Test sending chat message"""
    response = client.post(
        "/chat/message",
        headers=auth_headers,
        json={"message": "Hello, how are you?"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "model" in data


def test_nexo_paisa_payment(client, auth_headers):
    """Test initiating Nexo Paisa payment"""
    response = client.post(
        "/nexo-paisa/pay",
        headers=auth_headers,
        json={
            "amount": 1000.0,
            "currency": "NPR",
            "description": "Test payment"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "transaction_id" in data
    assert "status" in data
