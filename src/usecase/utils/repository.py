from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import delete, func, insert, select, update
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
            record_dict = {
                column_name: value
                for column_name, value in zip(column_names, inserted_record)
            }
            return record_dict
        else:
            return None

    async def edit_one(self, id: int, data: dict) -> int:
        stmt = (
            update(self.model)
            .values(**data)
            .filter_by(id=id)
            .returning(*self.model.__table__.c)
        )
        res = await self.session.execute(stmt)
        updated_record = res.fetchone()
        if updated_record:
            column_names = self.model.__table__.c.keys()
            record_dict = {
                column_name: value
                for column_name, value in zip(column_names, updated_record)
            }
            return record_dict
        else:
            return None

    async def find_all(
        self,
        organization_id: int = None,
        begin_date: datetime = None,
        end_date: datetime = None,
        note_id: int = None,
        
    ):
        stmt = select(self.model).where(self.model.isDelete == False)
        if organization_id:
            stmt = stmt.where(self.model.organizationId == organization_id)

        # Add date range condition only if both start_date and end_date are provided
        if begin_date is not None and end_date is not None:
            stmt = stmt.where(self.model.createdAt.between(begin_date, end_date))

        if note_id:
            stmt = stmt.where(self.model.noteId == note_id)

        res = await self.session.execute(stmt)
        res = [row[0].to_read_model_as_list(self.session) for row in res.all()]
        return res

    async def find_one(self, id: int):
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        result = res.scalar_one_or_none()
        if result:
            return result.to_read_model_as_detail()
        else:
            return None

    async def delete_note_users(self, id: int):
        stmt = delete(self.model).where(self.model.noteId == id)
        await self.session.execute(stmt)
        await self.session.commit()
    
    async def count_note_users(self, note_id: int):
        stmt = select(func.count()).select_from(self.model).where(self.model.noteId == note_id)
        res = await self.session.execute(stmt)
        count = res.scalar()
        return count

