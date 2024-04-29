from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.usecase.schemas.notes import NoteSchemaAddResponse


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError
    
    @abstractmethod
    async def find_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> NoteSchemaAddResponse:
        stmt = insert(self.model).values(**data).returning(*self.model.__table__.c)
        res = await self.session.execute(stmt)
        inserted_record = res.fetchone()
        if inserted_record:
            column_names = self.model.__table__.c.keys()
            record_dict = {column_name: value for column_name, value in zip(column_names, inserted_record)}
            return record_dict
        else:
            return None

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=id).returning(self.model.id, self.model.title)
        res = await self.session.execute(stmt)
        return res.scalar_one()
    
    async def find_all(self):
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res
    
    async def find_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = res.scalar_one().to_read_model()
        return res