from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Dans un vrai projet, l'URL viendrait des variables d'environnement (pydantic-settings)
# Pour l'instant on hardcode une URL PostgreSQL asynchrone (asyncpg)
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_crud"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db_session():
    """
    Dépendance FastAPI pour injecter la session de base de données.
    C'est ici qu'on gère le cycle de vie de la connexion à la DB.
    """
    async with async_session_maker() as session:
        yield session
