from datetime import datetime
from typing import Annotated

import pytest
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import clear_mappers, declarative_base, sessionmaker

from src.app.config import settings
from src.usecase.api.dependencies import UOWDep
from src.usecase.utils.repository import SQLAlchemyRepository
from src.usecase.utils.unitofwork import IUnitOfWork, UnitOfWork

DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

Base = declarative_base()
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def uow():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        async with session.begin():
            yield UnitOfWork(session)


@pytest.mark.asyncio
async def test_add_one(uow: Annotated[IUnitOfWork, Depends(UnitOfWork)]):
    note_data = {
        "organizationId": 1,
        "title": "Test Note",
        "date": datetime(2024, 5, 10).date(),
        "fromTime": datetime(2024, 5, 10, 9, 0, 0).time(),
        "tillTime": datetime(2024, 5, 10, 10, 0, 0).time(),
        "location": "Test Location",
        "description": "Test Description",
        "colorCode": "#FFFFFF",
        "ownerId": 123,
    }
    await uow.notes.add_one(note_data)
