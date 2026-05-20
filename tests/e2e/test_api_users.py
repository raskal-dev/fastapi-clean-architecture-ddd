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

def test_rbac_admin_only(client: TestClient, mock_user_repo):
    """
    Test E2E : Vérifie le RBAC sur la route GET /users/
    """
    # 1. Inscription d'un utilisateur normal
    client.post("/api/v1/users/", json={"email": "user@test.com", "password": "pwd"})
    token_user = client.post("/api/v1/auth/token", data={"username": "user@test.com", "password": "pwd"}).json()["access_token"]
    
    # 2. Tentative d'accès à la route admin par l'utilisateur normal
    headers_user = {"Authorization": f"Bearer {token_user}"}
    response_forbidden = client.get("/api/v1/users/", headers=headers_user)
    assert response_forbidden.status_code == 403 # L'accès doit être refusé
    
    # 3. Élévation de privilèges (en manipulant le Mock DB pour le test)
    user_entity = list(mock_user_repo.users.values())[0]
    from app.domain.entities.user import UserRole
    user_entity.role = UserRole.ADMIN
    
    # 4. On redemande un token (le payload contiendra le nouveau rôle)
    token_admin = client.post("/api/v1/auth/token", data={"username": "user@test.com", "password": "pwd"}).json()["access_token"]
    
    # 5. Tentative d'accès en tant qu'ADMIN
    headers_admin = {"Authorization": f"Bearer {token_admin}"}
    response_success = client.get("/api/v1/users/", headers=headers_admin)
    
    assert response_success.status_code == 200
    assert isinstance(response_success.json(), list)
