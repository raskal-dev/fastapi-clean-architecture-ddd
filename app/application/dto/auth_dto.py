from pydantic import BaseModel


class TokenDTO(BaseModel):
    """
    Format de réponse attendu par OAuth2.
    Il FAUT retourner `access_token` et `token_type`.
    """
    access_token: str
    token_type: str = "bearer"
