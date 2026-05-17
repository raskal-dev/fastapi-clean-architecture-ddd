from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.infrastructure.config.settings import settings

# On utilise l'URL dynamique générée depuis notre .env !
engine = create_async_engine(settings.database_url, echo=(settings.app_env == "development"))
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db_session():
    """
    Dépendance FastAPI pour injecter la session de base de données.
    C'est ici qu'on gère le cycle de vie de la connexion à la DB.
    """
    async with async_session_maker() as session:
        yield session
