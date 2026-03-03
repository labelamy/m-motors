def test_get_vehicles(client):
    response = client.get("/vehicules/")
    assert response.status_code == 200