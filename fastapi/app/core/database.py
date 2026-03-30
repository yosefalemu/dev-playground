import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    # Neon recommends pre-ping to handle connections that 
    # might be closed by their "scale-to-zero" feature.
    pool_pre_ping=True 
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)