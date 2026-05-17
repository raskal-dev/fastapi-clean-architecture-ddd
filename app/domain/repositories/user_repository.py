import uuid
from typing import Optional, Protocol

from app.domain.entities.user import User


class UserRepository(Protocol):
    """
    Interface (Port) pour le repository User.
    Définit le contrat que toute implémentation concrète (ex: PostgreSQL) devra respecter.
    """

    async def create(self, user: User) -> User:
        """Crée un nouvel utilisateur."""
        ...

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Récupère un utilisateur par son ID."""
        ...

    async def get_by_email(self, email: str) -> Optional[User]:
        """Récupère un utilisateur par son email."""
        ...
