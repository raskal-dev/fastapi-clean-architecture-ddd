import uuid

from typing import Callable, Sequence

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.config.settings import settings
from app.infrastructure.database.session import get_db_session
from app.infrastructure.repositories.postgres_user_repository import PostgresUserRepository
from app.infrastructure.security.jwt_service import verify_token

# C'est ce qui indique à Swagger UI où aller chercher le token (la route /auth/token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/token")

async def get_user_repository(session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    """Injection de l'interface UserRepository."""
    return PostgresUserRepository(session)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repository: UserRepository = Depends(get_user_repository)
) -> User:
    """
    Dépendance (Middleware) pour sécuriser les routes.
    FastAPI exécutera cette fonction AVANT d'entrer dans ta route.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants (token) invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 1. Décoder le token
    payload = verify_token(token)
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise credentials_exception

    try:
        user_id = uuid.UUID(user_id_str)
    except ValueError:
        raise credentials_exception

    # 2. Chercher l'utilisateur en base de données via l'interface
    user = await repository.get_by_id(user_id)
    
    if user is None or not user.is_active:
        raise credentials_exception
        
    return user

def require_role(allowed_roles: Sequence[str]) -> Callable:
    """
    Crée une dépendance FastAPI qui vérifie le rôle de l'utilisateur.
    Utilisation: `Depends(require_role(["ADMIN"]))`
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        # On vérifie si la valeur string du rôle de l'utilisateur est dans la liste
        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'avez pas les permissions nécessaires."
            )
        return current_user
    return role_checker
