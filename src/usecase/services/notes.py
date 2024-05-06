from datetime import datetime

from src.infrastructure.postgres.node_dto import Note
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
        async with uow:
            note = await uow.notes.add_one(notes_dict)
            for user_id in user_ids:
                note_user_dict = {
                    "userId": user_id,
                    "fullName": "Dilshod Bakhtiyorov",
                    "noteId": note.get("id"),
                }
                await uow.note_users.add_one(note_user_dict)
            await uow.commit()
            note_obj = Note(**note).to_read_model_as_list()
            note_obj["usersCount"] = len(user_ids)
            return note_obj

    async def get_notes(
        self,
        organization_id: int,
        uow: IUnitOfWork,
        begin_date: datetime,
        end_date: datetime,
    ):
        async with uow:
            notes = await uow.notes.find_all(
                begin_date=begin_date,
                end_date=end_date,
                organization_id=organization_id,
            )
            for note in notes:
                users_count = await uow.note_users.count_note_users(
                    note_id=note.get("id")
                )
                note["usersCount"] = users_count
            return notes

    async def edit_note(self, uow: IUnitOfWork, note_id: int, note: NoteSchemaEdit):
        notes_dict = note.model_dump()
        note_user_ids = notes_dict.pop("userIds", [])
        # note_users = []
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
                await uow.note_users.add_one(note_user_dict)
                # note_users.append(note_user)
            await uow.commit()
            # updated_note.update({"users": note_users})
            note_obj = Note(**updated_note).to_read_model_as_list()
            note_obj["usersCount"] = len(note_user_ids)
            return note_obj

    async def get_note(self, uow: IUnitOfWork, note_id: int):
        note_users = []
        note_user_obj = NoteUserService()

        async with uow:
            note = await uow.notes.find_one(note_id)
            note_users = await note_user_obj.get_note_users(uow, note_id)

        note_with_users = {**note, "users": note_users}
        return note_with_users


class NoteUserService:
    async def get_note_users(self, uow: IUnitOfWork, note_id: int):
        async with uow:
            note_users = await uow.note_users.find_all(note_id=note_id)
            return note_users
