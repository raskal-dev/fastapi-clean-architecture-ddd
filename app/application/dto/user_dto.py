import uuid
from datetime import datetime

from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.entities.user import UserRole


class UserCreateDTO(BaseModel):
    """
    Data Transfer Object (DTO) pour la création d'un utilisateur.
    On valide ici le format (ex: EmailStr garantit que c'est un email valide).
    """
    email: EmailStr
    password: str = Field(..., max_length=72, description="Le mot de passe (limite bcrypt 72 caractères)")


class UserResponseDTO(BaseModel):
    """
    DTO pour la réponse renvoyée au client.
    Très important : on ne renvoie jamais le `hashed_password` !
    """
    id: uuid.UUID
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

    # Permet à Pydantic de lire les données depuis notre Entité ou Modèle SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


class UserUpdateDTO(BaseModel):
    """
    DTO pour la mise à jour (PATCH).
    Tous les champs sont optionnels, on ne met à jour que ce qui est fourni.
    """
    password: Optional[str] = Field(None, max_length=72, description="Nouveau mot de passe")
