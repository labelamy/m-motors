def test_admin_access_denied(client):
    client.post("/auth/register", json={
        "email": "user2@test.com",
        "password": "123456"
    })

    login = client.post("/auth/login", json={
        "email": "user2@test.com",
        "password": "123456"
    })

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/dossiers/admin", headers=headers)
    assert response.status_code == 403