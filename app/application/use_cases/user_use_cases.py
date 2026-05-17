from passlib.context import CryptContext

from app.application.dto.user_dto import UserCreateDTO, UserResponseDTO
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

# Configuration de base pour le hashing.
# Normalement, ceci serait injecté via un service d'infrastructure (ex: IPasswordHasher).
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserUseCases:
    """
    Le chef d'orchestre. C'est ici qu'on définit "l'histoire" de notre application.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Inversion de dépendance : On injecte l'interface (Port) UserRepository.
        Le Use Case se fiche éperdument de savoir si derrière c'est PostgreSQL ou un fichier texte.
        """
        self.user_repository = user_repository

    async def register_user(self, dto: UserCreateDTO) -> UserResponseDTO:
        """Cas d'usage : Inscrire un nouvel utilisateur."""
        
        # 1. Règle métier : l'email doit être unique
        existing_user = await self.user_repository.get_by_email(dto.email)
        if existing_user:
            raise ValueError("Un utilisateur avec cet email existe déjà.")

        # 2. Sécurité : hasher le mot de passe
        hashed_password = pwd_context.hash(dto.password)

        # 3. Création : Instancier notre Entité (cœur pur)
        user_entity = User(
            email=dto.email,
            hashed_password=hashed_password
        )

        # 4. Persistance : On délègue à l'infrastructure via l'interface
        saved_user = await self.user_repository.create(user_entity)

        # 5. Retour : On transforme notre Entité métier en DTO pour l'API
        return UserResponseDTO.model_validate(saved_user)
