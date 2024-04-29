from abc import ABC, abstractmethod
from typing import Type

from src.infrastructure.postgres.database import async_session
from src.usecase.repositories.note import *


# https://github1s.com/cosmicpython/code/tree/chapter_06_uow
class IUnitOfWork(ABC):
    notes: Type[NotesRepository]
    note_users: Type[NoteUsersRepository]
    
    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session

    async def __aenter__(self):
        from src.usecase.repositories.note import NotesRepository, NoteUsersRepository
        self.session = self.session_factory()

        self.notes = NotesRepository(self.session)
        self.note_users = NoteUsersRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()