from app.application.dto.auth_dto import TokenDTO
from app.application.use_cases.user_use_cases import pwd_context
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.jwt_service import create_access_token


class AuthUseCases:
    """Cas d'usage liés à l'authentification."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def login(self, email: str, plain_password: str) -> TokenDTO:
        """
        Vérifie les identifiants et retourne un token JWT.
        Lève une ValueError si les identifiants sont invalides.
        """
        # 1. Chercher l'utilisateur par son email
        user = await self.user_repository.get_by_email(email)
        if not user or not user.is_active:
            # On ne donne pas d'indice si c'est l'email ou le mdp qui est faux (sécurité)
            raise ValueError("Email ou mot de passe incorrect.")

        # 2. Vérifier le mot de passe avec Argon2
        if not pwd_context.verify(plain_password, user.hashed_password):
            raise ValueError("Email ou mot de passe incorrect.")

        # 3. Générer le JWT
        # On utilise "sub" (subject) pour stocker l'ID de l'utilisateur, c'est le standard JWT
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return TokenDTO(access_token=access_token)
