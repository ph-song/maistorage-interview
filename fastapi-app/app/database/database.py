from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel
from app.core.settings import settings

# 1. Create an ASYNC engine for SQLite
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, 
    connect_args={"check_same_thread": False}
)

# 2. Define an ASYNC session maker
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False, 
    autocommit=False, 
    autoflush=False
)

async def create_db_and_tables():
    # In async, we must run the DDL in a sync context within run_sync
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db

# 3. Export the ASYNC annotated dependency
DbSession = Annotated[AsyncSession, Depends(get_db)]
