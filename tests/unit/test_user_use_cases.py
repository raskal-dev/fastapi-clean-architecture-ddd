import pytest

from app.application.dto.user_dto import UserCreateDTO
from app.application.use_cases.user_use_cases import UserUseCases


@pytest.mark.asyncio
async def test_register_user_success(mock_user_repo):
    """
    Test unitaire : Inscription réussie.
    On vérifie que les règles métier s'exécutent correctement sans base de données réelle.
    """
    # 1. Arrange (Préparation)
    use_cases = UserUseCases(user_repository=mock_user_repo)
    dto = UserCreateDTO(email="test@clean.com", password="super_password")
    
    # 2. Act (Action)
    response = await use_cases.register_user(dto)
    
    # 3. Assert (Vérification)
    assert response.email == "test@clean.com"
    assert response.is_active is True
    assert response.id is not None
    # Vérifie que l'utilisateur est bien stocké dans le Mock
    assert len(mock_user_repo.users) == 1
    stored_user = list(mock_user_repo.users.values())[0]
    assert stored_user.email == "test@clean.com"


@pytest.mark.asyncio
async def test_register_user_duplicate_email(mock_user_repo):
    """
    Test unitaire : Inscription avec un email déjà existant.
    On s'attend à une levée d'exception (ValueError).
    """
    # Arrange
    use_cases = UserUseCases(user_repository=mock_user_repo)
    dto = UserCreateDTO(email="duplicate@clean.com", password="super_password")
    await use_cases.register_user(dto) # Premier insert réussi
    
    # Act & Assert
    with pytest.raises(ValueError) as exc:
        await use_cases.register_user(dto) # Deuxième tentative
        
    assert str(exc.value) == "Un utilisateur avec cet email existe déjà."

@pytest.mark.asyncio
async def test_get_all_users(mock_user_repo):
    """
    Test unitaire : Récupération de tous les utilisateurs.
    """
    use_cases = UserUseCases(user_repository=mock_user_repo)
    
    # 1. On crée deux utilisateurs
    await use_cases.register_user(UserCreateDTO(email="user1@test.com", password="pwd"))
    await use_cases.register_user(UserCreateDTO(email="user2@test.com", password="pwd"))
    
    # 2. On récupère tout
    users = await use_cases.get_all_users()
    
    # 3. Vérification
    assert len(users) == 2
    assert users[0].email == "user1@test.com"
