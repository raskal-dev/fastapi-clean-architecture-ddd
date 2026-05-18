import uuid
from datetime import datetime, timezone
from typing import Optional

import pytest
from fastapi.testclient import TestClient

from app.application.use_cases.auth_use_cases import AuthUseCases
from app.application.use_cases.user_use_cases import UserUseCases
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.main import app
from app.presentation.api.dependencies.auth_deps import get_user_repository
from app.presentation.api.routes.auth import get_auth_use_cases
from app.presentation.api.routes.users import get_user_use_cases


class MockUserRepository(UserRepository):
    """
    Mock en mémoire de notre base de données.
    C'est l'avantage ultime de la Clean Architecture !
    """
    def __init__(self):
        self.users = {}

    async def create(self, user: User) -> User:
        user.id = uuid.uuid4()
        user.created_at = datetime.now(timezone.utc)
        user.updated_at = datetime.now(timezone.utc)
        self.users[user.id] = user
        return user

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        return self.users.get(user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    async def update(self, user: User) -> User:
        self.users[user.id] = user
        return user


@pytest.fixture
def mock_user_repo():
    """Fixture qui fournit un MockUserRepository tout neuf pour chaque test."""
    return MockUserRepository()


@pytest.fixture
def client(mock_user_repo):
    """
    FastAPI TestClient configuré pour utiliser notre Mock DB.
    On utilise `dependency_overrides` pour injecter nos mocks à la place des vraies dépendances.
    """
    def override_get_user_use_cases():
        return UserUseCases(user_repository=mock_user_repo)
        
    def override_get_auth_use_cases():
        return AuthUseCases(user_repository=mock_user_repo)
        
    def override_get_user_repository():
        return mock_user_repo

    app.dependency_overrides[get_user_use_cases] = override_get_user_use_cases
    app.dependency_overrides[get_auth_use_cases] = override_get_auth_use_cases
    app.dependency_overrides[get_user_repository] = override_get_user_repository

    yield TestClient(app)
    
    # Nettoyage après le test
    app.dependency_overrides.clear()
