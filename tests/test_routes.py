def payload(**overrides):
    data = {
        "name": "Anita Rao",
        "email": "anita@example.com",
        "address": "Pune, India",
        "phone_number": "9876543210",
    }
    data.update(overrides)
    return data

def test_create_account(client):
    response = client.post("/accounts", json=payload())
    assert response.status_code == 201
    assert response.get_json()["email"] == "anita@example.com"

def test_list_accounts(client):
    client.post("/accounts", json=payload())
    response = client.get("/accounts")
    assert response.status_code == 200
    assert len(response.get_json()) == 1

def test_read_account(client):
    created = client.post("/accounts", json=payload()).get_json()
    response = client.get(f"/accounts/{created['id']}")
    assert response.status_code == 200
    assert response.get_json()["id"] == created["id"]

def test_read_missing_account(client):
    assert client.get("/accounts/999").status_code == 404

def test_update_account(client):
    created = client.post("/accounts", json=payload()).get_json()
    response = client.put(f"/accounts/{created['id']}", json={"name": "Anita Updated"})
    assert response.status_code == 200
    assert response.get_json()["name"] == "Anita Updated"

def test_delete_account(client):
    created = client.post("/accounts", json=payload()).get_json()
    response = client.delete(f"/accounts/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/accounts/{created['id']}").status_code == 404

def test_create_missing_required_field(client):
    response = client.post("/accounts", json={"name": "Missing fields"})
    assert response.status_code == 400
