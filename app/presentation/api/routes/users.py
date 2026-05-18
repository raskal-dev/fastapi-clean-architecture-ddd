from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.user_dto import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from app.application.use_cases.user_use_cases import UserUseCases
from app.domain.entities.user import User
from app.infrastructure.database.session import get_db_session
from app.infrastructure.repositories.postgres_user_repository import PostgresUserRepository
from app.presentation.api.dependencies.auth_deps import get_current_user

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

@router.get("/me", response_model=UserResponseDTO)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Route Sécurisée : Récupère les informations de l'utilisateur connecté.
    Le simple fait d'ajouter `Depends(get_current_user)` garantit que 
    FastAPI rejettera la requête (401) s'il n'y a pas de token valide !
    """
    # L'entité métier `current_user` est magiquement transformée 
    # en `UserResponseDTO` par Pydantic.
    return current_user

@router.patch("/me", response_model=UserResponseDTO)
async def update_users_me(
    user_update: UserUpdateDTO,
    current_user: User = Depends(get_current_user),
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """
    Route Sécurisée : Met à jour le profil de l'utilisateur connecté.
    Pour l'instant, permet uniquement de changer le mot de passe.
    """
    return await use_cases.update_user(current_user, user_update)

@router.delete("/me", response_model=UserResponseDTO)
async def delete_users_me(
    current_user: User = Depends(get_current_user),
    use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """
    Route Sécurisée : Désactive le compte de l'utilisateur connecté (Soft Delete).
    L'utilisateur ne sera pas supprimé de la base de données, mais son `is_active` passera à false.
    """
    return await use_cases.deactivate_user(current_user)
