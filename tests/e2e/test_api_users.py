from fastapi.testclient import TestClient

def test_create_user_endpoint(client: TestClient):
    """
    Test E2E : Création d'un utilisateur via l'API (POST /users/).
    Le client HTTP tape sur la vraie route, mais la DB est mockée grâce au dependency_overrides.
    """
    payload = {
        "email": "e2e@fastapi.com",
        "password": "password123"
    }
    
    response = client.post("/api/v1/users/", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "e2e@fastapi.com"
    assert "id" in data
    assert "hashed_password" not in data # Sécurité : le hash ne doit jamais fuiter


def test_protected_route_without_token(client: TestClient):
    """
    Test E2E : Accès à une route protégée sans JWT.
    """
    response = client.get("/api/v1/users/me")
    
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_full_login_flow(client: TestClient):
    """
    Test E2E complet : Inscription -> Login -> Accès profil
    """
    # 1. Inscription
    client.post("/api/v1/users/", json={"email": "flow@test.com", "password": "pwd"})
    
    # 2. Login
    login_response = client.post(
        "/api/v1/auth/token",
        data={"username": "flow@test.com", "password": "pwd"} # OAuth2 attend form-data
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # 3. Accès profil avec JWT
    headers = {"Authorization": f"Bearer {token}"}
    me_response = client.get("/api/v1/users/me", headers=headers)
    
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "flow@test.com"
