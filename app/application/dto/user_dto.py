import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreateDTO(BaseModel):
    """
    Data Transfer Object (DTO) pour la création d'un utilisateur.
    On valide ici le format (ex: EmailStr garantit que c'est un email valide).
    """
    email: EmailStr
    password: str


class UserResponseDTO(BaseModel):
    """
    DTO pour la réponse renvoyée au client.
    Très important : on ne renvoie jamais le `hashed_password` !
    """
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Permet à Pydantic de lire les données depuis notre Entité ou Modèle SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
