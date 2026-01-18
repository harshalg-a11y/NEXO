"""Test configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db import Base, get_db
from app.models.user import User
from app.models.contact import Contact
from app.models.car import Car
from app.models.car_booking import CarBooking
from app.models.hotel_booking import HotelBooking
from app.models.nexo_paisa_transaction import NexoPaisaTransaction
from app.security import hash_password

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client with database session override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        email="test@example.com",
        hashed_password=hash_password("testpassword123"),
        full_name="Test User",
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_user(db_session):
    """Create an admin user"""
    user = User(
        email="admin@example.com",
        hashed_password=hash_password("adminpassword123"),
        full_name="Admin User",
        role="admin"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(client, test_user):
    """Get auth headers with valid JWT token"""
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_auth_headers(client, admin_user):
    """Get auth headers for admin user"""
    response = client.post(
        "/auth/login",
        json={"email": "admin@example.com", "password": "adminpassword123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
