import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register():
    unique_email = f"{uuid.uuid4()}@test.com"

    response = client.post("/auth/register", json={
        "email": unique_email,
        "password": "123456"
    })

    assert response.status_code == 200