import pytest
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqllite.users_db import Base, User
from server import app, get_db
from utils.token import SECRET_KEY, ALGORITHM
import jwt

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_user():
    res = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert res.status_code == 200
    assert res.json()["msg"] == "User created"


def test_register_existing_user():
    res = client.post("/register", json={"username": "testuser", "password": "testpass"})
    assert res.status_code == 400
    assert res.json()["detail"] == "Username already exists"


def test_login_valid_user():
    res = client.post("/login", json={"username": "testuser", "password": "testpass"})
    assert res.status_code == 200
    tokens = res.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    global ACCESS_TOKEN, REFRESH_TOKEN
    ACCESS_TOKEN = tokens["access_token"]
    REFRESH_TOKEN = tokens["refresh_token"]


def test_login_invalid_password():
    res = client.post("/login", json={"username": "testuser", "password": "wrongpass"})
    assert res.status_code == 401
    assert res.json()["detail"] == "Invalid credentials"


def test_renew_valid_refresh_token():
    res = client.post("/renew", json={"refresh_token": REFRESH_TOKEN})
    assert res.status_code == 200
    tokens = res.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens


def test_renew_invalid_refresh_token():
    res = client.post("/renew", json={"refresh_token": "fake.token.string"})
    assert res.status_code == 401
    assert res.json()["detail"] in ["Invalid refresh token", "Refresh token expired"]


def test_analyze_endpoint_for_auth():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    res = client.post("/analyze", json={"code": "print('Hello')"}, headers=headers)

    assert res.status_code == 200
    data = res.json()
    assert "static" in data
    assert "ai" in data


def test_analyze_with_valid_jwt_header():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    res = client.post("/analyze", json={"code": "print(123)"}, headers=headers)
    assert res.status_code == 200


def test_analyze_with_invalid_jwt_header():
    headers = {"Authorization": "Bearer invalid.token"}
    res = client.post("/analyze", json={"code": "print(123)"}, headers=headers)
    assert res.status_code in [401, 403]
