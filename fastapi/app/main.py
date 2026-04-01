from contextlib import asynccontextmanager
from fastapi import FastAPI, Request,responses
from app.core.database import engine
from app.domain.exceptions.product_exc import InsufficientStockException, ProductAlreadyExistsException, ProductNotFoundException, ProductOutofStockException
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

@app.exception_handler(ProductNotFoundException)
async def product_not_found_exception_handler(request: Request, exc: ProductNotFoundException):
    return responses.JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(ProductAlreadyExistsException)
async def product_already_exists_exception_handler(request: Request, exc: ProductAlreadyExistsException):
    return responses.JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(ProductOutofStockException)
async def product_out_of_stock_exception_handler(request: Request, exc: ProductOutofStockException):
    return responses.JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(InsufficientStockException)
async def insufficient_stock_exception_handler(request: Request, exc: InsufficientStockException):
    return responses.JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return responses.JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred"}
    )