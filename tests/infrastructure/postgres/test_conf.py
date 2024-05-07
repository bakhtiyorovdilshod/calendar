# conftest.py

from datetime import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import clear_mappers, declarative_base, sessionmaker

from src.app.config import settings
from src.usecase.utils.repository import SQLAlchemyRepository
from src.usecase.utils.unitofwork import UnitOfWork

# Configure test database URL
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

# Create an asynchronous database engine
engine = create_async_engine(TEST_DATABASE_URL)

# Create a base class for declarative data models
Base = declarative_base()

# Create an async sessionmaker
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Define fixture to set up the test database
@pytest.fixture(scope="session")
async def async_db():
    # Create test database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    # Drop test database tables after all tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Define fixture to create an async session
@pytest.fixture
async def async_session(async_db):
    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def repository(async_session):
    async with async_session() as session:
        yield SQLAlchemyRepository(session)
