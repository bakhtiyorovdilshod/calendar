from datetime import datetime

from fastapi.responses import JSONResponse

from src.app.clients.state.staff import StateClient
from src.app.error import CustomHTTPException
from src.infrastructure.postgres.node_dto import Note
from src.usecase.schemas.notes import NoteSchema, NoteSchemaAdd, NoteSchemaEdit
from src.usecase.utils.repository import AbstractRepository
from src.usecase.utils.unitofwork import IUnitOfWork


class NotesService:
    async def add_note(
        self, uow: IUnitOfWork, note: NoteSchemaAdd, organization_id: int, pinfl: str
    ):
        notes_dict = note.model_dump()
        user_ids = notes_dict.pop("userIds")
        if pinfl not in user_ids:
            user_ids.append(pinfl)
        state_client = StateClient()
        users_info = await state_client.employee_validate(
            pinfls=user_ids, organization_id=organization_id
        )
        print(users_info)
        notes_dict.update({"organizationId": organization_id, "ownerId": pinfl})
        async with uow:
            note = await uow.notes.add_one(notes_dict)
            for user_obj in users_info:
                note_user_dict = {
                    "fullName": user_obj.get("full_name"),
                    "noteId": note.get("id"),
                    "pinfl": user_obj.get('pinfl'),
                    "image": user_obj.get('image')
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
        pinfl: str,
    ):
        async with uow:
            note_ids = await uow.note_users.get_note_ids(pinfl=pinfl)
            notes = await uow.notes.find_all(
                begin_date=begin_date,
                end_date=end_date,
                organization_id=organization_id,
                note_ids=note_ids
            )
            for note in notes:
                users_count = await uow.note_users.count_note_users(
                    note_id=note.get("id")
                )
                note["usersCount"] = users_count
            return notes

    async def edit_note(
        self, uow: IUnitOfWork, note_id: int, note: NoteSchemaEdit, organization_id: int, pinfl: str
    ):
        notes_dict = note.model_dump()
        note_user_ids = notes_dict.pop("userIds", [])
        if pinfl not in note_user_ids:
            note_user_ids.append(pinfl)
        state_client = StateClient()
        users_info = await state_client.employee_validate(
            pinfls=note_user_ids, organization_id=organization_id
        )
        async with uow:
            if len(note_user_ids) != 0:
                await uow.note_users.delete_note_users(note_id)
            updated_note = await uow.notes.edit_one(note_id, notes_dict)
            if not updated_note:
                raise CustomHTTPException(status_code=404, detail="note has not found")
            for user_obj in users_info:
                note_user_dict = {
                    "userId": user_obj.get("user_id"),
                    "fullName": user_obj.get("full_name"),
                    "noteId": note_id,
                    "pinfl": user_obj.get('pinfl'),
                    "image": user_obj.get('image')
                }
                await uow.note_users.add_one(note_user_dict)
                # note_users.append(note_user)
            await uow.commit()
            # updated_note.update({"users": note_users})
            note_obj = Note(**updated_note).to_read_model_as_list()
            note_obj["usersCount"] = len(note_user_ids)
            return note_obj

    async def get_note(self, uow: IUnitOfWork, note_id: int, owner_id):
        note_users = []
        note_user_obj = NoteUserService()

        async with uow:
            note = await uow.notes.find_one(note_id)
            if not note:
                raise CustomHTTPException(status_code=404, detail="note has not found")
            note_users = await note_user_obj.get_note_users(uow, note_id)
            note['isOwner'] = True if note.get('ownerId') == owner_id else False

        note_with_users = {**note, "users": note_users}
        return note_with_users

    async def delete_note(self, uow: IUnitOfWork, note_id: int):
        message = {"status": "note has been deleted"}
        async with uow:
            note = await uow.notes.find_one(note_id)
            if not note:
                raise CustomHTTPException(status_code=404, detail="note has not found")
            await uow.note_users.delete_note_users(note_id)
            await uow.notes.delete_one(note_id)
        return message


class NoteUserService:
    async def get_note_users(self, uow: IUnitOfWork, note_id: int):
        async with uow:
            note_users = await uow.note_users.find_all(note_id=note_id)
            return note_users