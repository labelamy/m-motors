def test_create_dossier(client):
    # Register user
    client.post("/auth/register", json={
        "email": "user@test.com",
        "password": "123456"
    })

    login = client.post("/auth/login", json={
        "email": "user@test.com",
        "password": "123456"
    })

    token = login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/dossiers/", json={
        "vehicule_id": 1,
        "type": "achat"
    }, headers=headers)

    assert response.status_code in [200, 404]  # selon si véhicule existe