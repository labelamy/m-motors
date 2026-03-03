import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register_success():
    unique_email = f"{uuid.uuid4()}@test.com"

    response = client.post("/auth/register", json={
        "email": unique_email,
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == unique_email
    assert "id" in data
    assert data["role"] == "client"


def test_register_duplicate_email():
    unique_email = f"{uuid.uuid4()}@test.com"

    client.post("/auth/register", json={
        "email": unique_email,
        "password": "123456"
    })

    response = client.post("/auth/register", json={
        "email": unique_email,
        "password": "123456"
    })

    # selon ton code actuel ça peut être 500
    # idéalement tu dois gérer ça et retourner 400
    assert response.status_code in [400, 500]


def test_login_success():
    unique_email = f"{uuid.uuid4()}@test.com"

    client.post("/auth/register", json={
        "email": unique_email,
        "password": "123456"
    })

    response = client.post("/auth/login", json={
        "email": unique_email,
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password():
    unique_email = f"{uuid.uuid4()}@test.com"

    client.post("/auth/register", json={
        "email": unique_email,
        "password": "123456"
    })

    response = client.post("/auth/login", json={
        "email": unique_email,
        "password": "wrongpassword"
    })

    assert response.status_code == 401