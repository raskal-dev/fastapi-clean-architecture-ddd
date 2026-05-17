from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.database.session import Base, engine
# Assurons-nous d'importer les modèles pour que metadata.create_all les voie
from app.infrastructure.database.models import user_model
from app.presentation.api.routes import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestion du cycle de vie de l'application FastAPI.
    Ici, on crée les tables dans la base de données au démarrage.
    (Note: En production, on utiliserait Alembic pour gérer les migrations).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title="FastAPI CRUD - Clean Architecture",
    description="API construite avec les principes du Domain Driven Design (DDD).",
    version="0.1.0",
    lifespan=lifespan,
)

# On connecte le routeur de nos utilisateurs à l'application principale
app.include_router(users.router)


@app.get("/")
async def root():
    """Route par défaut pour vérifier que tout fonctionne."""
    return {
        "message": "Bienvenue sur l'API FastAPI Clean Architecture !",
        "docs": "Allez sur /docs pour explorer l'API avec Swagger UI."
    }
