import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.domain.exceptions.product_exc import DatabaseURLNotConfigured

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise DatabaseURLNotConfigured("Data base url is not configured!!!")

try:
    engine = create_async_engine(
        DATABASE_URL, 
        echo=True,
        # Neon recommends pre-ping to handle connections that 
        # might be closed by their "scale-to-zero" feature.
        pool_pre_ping=True 
    )
except Exception as e:
    print(f"Error creating database engine: {str(e)}")
    raise DatabaseURLNotConfigured(f"Failed to create database engine: {str(e)}")

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)