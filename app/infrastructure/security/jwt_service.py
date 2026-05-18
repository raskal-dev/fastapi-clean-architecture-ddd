from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from app.infrastructure.config.settings import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Génère un JWT signé pour l'authentification."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Valide et décode un JWT.
    Retourne le payload si valide, lève une exception (ou retourne un dict vide) sinon.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.PyJWTError:
        return {}
