from datetime import datetime

from src.usecase.schemas.notes import NoteSchema, NoteSchemaAdd, NoteSchemaEdit
from src.usecase.utils.repository import AbstractRepository
from src.usecase.utils.unitofwork import IUnitOfWork


class NotesService:
    async def add_note(
        self, uow: IUnitOfWork, note: NoteSchemaAdd, organization_id: int, owner_id: int
    ):
        notes_dict = note.model_dump()
        user_ids = notes_dict.pop("userIds")
        notes_dict.update({"organizationId": organization_id, "ownerId": owner_id})
        print(notes_dict)
        note_users = []
        async with uow:
            note = await uow.notes.add_one(notes_dict)
            for user_id in user_ids:
                note_user_dict = {
                    "userId": user_id,
                    "fullName": "Dilshod Bakhtiyorov",
                    "noteId": note.get("id"),
                }
                note_user = await uow.note_users.add_one(note_user_dict)
                note_users.append(note_user)
            await uow.commit()
            note.update({"users": note_users})
            return note

    async def get_notes(
        self, uow: IUnitOfWork, start_date: datetime = None, end_date: datetime = None
    ):
        async with uow:
            notes = await uow.notes.find_all(start_date=start_date, end_date=end_date)
            return notes

    async def edit_note(self, uow: IUnitOfWork, note_id: int, note: NoteSchemaEdit):
        notes_dict = note.model_dump()
        note_user_ids = notes_dict.pop("userIds", [])
        note_users = []
        async with uow:
            if len(note_user_ids) != 0:
                await uow.note_users.delete_note_users(note_id)
            updated_note = await uow.notes.edit_one(note_id, notes_dict)
            for user_id in note_user_ids:
                note_user_dict = {
                    "userId": user_id,
                    "fullName": "Dilshod Bakhtiyorov",
                    "noteId": updated_note.get("id"),
                }
                note_user = await uow.note_users.add_one(note_user_dict)
                note_users.append(note_user)
            await uow.commit()
            updated_note.update({"users": note_users})
            return updated_note

    async def get_note(self, uow: IUnitOfWork, note_id: int):
        note_users = []
        note_user_obj = NoteUserService()

        async with uow:
            note = await uow.notes.find_one(note_id)
            note_users = await note_user_obj.get_note_users(uow, note_id)

        note_with_users = {**note.dict(), "users": note_users}
        return note_with_users


class NoteUserService:
    async def get_note_users(self, uow: IUnitOfWork, note_id: int):
        async with uow:
            note_users = await uow.note_users.find_all(note_id=note_id)
            return note_users
