from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.user_dto import UserCreateDTO, UserResponseDTO
from app.application.use_cases.user_use_cases import UserUseCases
from app.infrastructure.database.session import get_db_session
from app.infrastructure.repositories.postgres_user_repository import PostgresUserRepository

router = APIRouter(prefix="/users", tags=["Users"])


async def get_user_use_cases(session: AsyncSession = Depends(get_db_session)) -> UserUseCases:
    """
    Injection de dépendances (Dependency Injection).
    C'est ici qu'on assemble les pièces du puzzle :
    Session DB -> Repository PostgreSQL -> Use Case
    """
    repository = PostgresUserRepository(session)
    return UserUseCases(user_repository=repository)


@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateDTO,
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """
    Endpoint HTTP pour créer un utilisateur.
    Remarque : Il n'y a AUCUNE logique métier ici. FastAPI sert juste de "Delivery Mechanism"
    pour transférer la requête HTTP vers notre logique applicative.
    """
    try:
        # On passe le relai à la couche Application
        return await use_cases.register_user(user_data)
    except ValueError as e:
        # Si une règle métier n'est pas respectée (ex: email existant)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
