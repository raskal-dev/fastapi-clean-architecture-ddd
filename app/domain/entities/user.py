import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

class UserRole(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"

@dataclass
class User:
    """
    Entité Métier (Entity) User.
    Cœur de la logique métier, indépendant de tout framework (SQLAlchemy, FastAPI).
    """
    email: str
    hashed_password: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
