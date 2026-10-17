def test_register_returns_user_without_password(client):
    response = client.post("/users/register", json={"email": "Asha@Example.com", "password": "strongpass1"})
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "asha@example.com"
    assert "password" not in body
    assert "hashed_password" not in body


def test_register_duplicate_email_returns_409(client):
    payload = {"email": "asha@example.com", "password": "strongpass1"}
    client.post("/users/register", json=payload)
    assert client.post("/users/register", json=payload).status_code == 409


def test_register_short_password_returns_422(client):
    response = client.post("/users/register", json={"email": "asha@example.com", "password": "short"})
    assert response.status_code == 422


def test_login_returns_token(client):
    client.post("/users/register", json={"email": "asha@example.com", "password": "strongpass1"})
    response = client.post("/users/login", data={"username": "asha@example.com", "password": "strongpass1"})
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_wrong_password_returns_401(client):
    client.post("/users/register", json={"email": "asha@example.com", "password": "strongpass1"})
    response = client.post("/users/login", data={"username": "asha@example.com", "password": "wrongpass1"})
    assert response.status_code == 401


def test_me_requires_token(client):
    assert client.get("/users/me").status_code == 401


def test_me_returns_current_user(client, make_headers):
    response = client.get("/users/me", headers=make_headers())
    assert response.status_code == 200
    assert response.json()["email"] == "asha@example.com"