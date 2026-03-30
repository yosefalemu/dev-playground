from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import engine
from app.infrastructure.db.models import Base
from app.presentation.routes import product_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This runs on startup: Creates tables in Neon
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # This runs on shutdown (optional)
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(product_routes.router)