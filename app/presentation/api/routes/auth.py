from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.auth_dto import TokenDTO
from app.application.use_cases.auth_use_cases import AuthUseCases
from app.infrastructure.database.session import get_db_session
from app.infrastructure.repositories.postgres_user_repository import PostgresUserRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])


async def get_auth_use_cases(session: AsyncSession = Depends(get_db_session)) -> AuthUseCases:
    """Injection de dépendance pour la connexion."""
    repository = PostgresUserRepository(session)
    return AuthUseCases(user_repository=repository)


@router.post("/token", response_model=TokenDTO)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_cases: AuthUseCases = Depends(get_auth_use_cases)
):
    """
    Endpoint OAuth2 standard pour s'authentifier.
    `OAuth2PasswordRequestForm` attend les champs `username` et `password`.
    Ici, notre 'username' est en fait l'email de l'utilisateur.
    """
    try:
        # On délègue toute la logique (hashing, vérification) au Use Case
        return await use_cases.login(email=form_data.username, plain_password=form_data.password)
    except ValueError as e:
        # En cas d'erreur (mauvais mdp, email inconnu)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
