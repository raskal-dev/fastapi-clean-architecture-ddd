from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Gestion centralisée et typée de la configuration via Pydantic.
    Pydantic va lire automatiquement le fichier .env et valider les types !
    """
    app_name: str
    app_env: str
    api_v1_prefix: str

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    # Configuration pour lire depuis le .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def database_url(self) -> str:
        """Construit l'URL SQLAlchemy asynchrone à partir des variables séparées."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


# On instancie les settings une seule fois (Singleton pattern)
settings = Settings()
