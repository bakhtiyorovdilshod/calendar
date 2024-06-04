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
        employment_ids = notes_dict.pop("employmentIds")
        state_client = StateClient()
        users_info = await state_client.employment_validate(
            employment_ids=employment_ids, organization_id=organization_id, pinfl=pinfl
        )
        notes_dict.update({"organizationId": organization_id})
        async with uow:
            note = await uow.notes.add_one(notes_dict)
            for user_obj in users_info:
                note_user_dict = {
                    "employmentId": user_obj.get("employmentId"),
                    "gender": user_obj.get("gender"),
                    "fullName": user_obj.get("fullName"),
                    "noteId": note.get("id"),
                    "pinfl": user_obj.get('pinfl'),
                    "image": user_obj.get('image'),
                    "isOwner": True if pinfl == user_obj.get('pinfl') else False,
                }
                await uow.note_users.add_one(note_user_dict)
            await uow.commit()
            note_obj = Note(**note).to_read_model_as_list()
            note_obj["usersCount"] = len(users_info)
            return note_obj

    async def get_notes(
        self,
        organization_id: int,
        uow: IUnitOfWork,
        begin_date: datetime,
        end_date: datetime,
        pinfl: str
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
        employment_ids = notes_dict.pop("employmentIds", [])
        state_client = StateClient()
        users_info = await state_client.employment_validate(
            employment_ids=employment_ids, organization_id=organization_id, pinfl=pinfl
        )
        async with uow:
            if len(employment_ids) != 0:
                await uow.note_users.delete_note_users(note_id)
            updated_note = await uow.notes.edit_one(note_id, notes_dict)
            if not updated_note:
                raise CustomHTTPException(status_code=404, detail="note has not found")
            for user_obj in users_info:
                if user_obj.get('pinfl') != pinfl:
                    note_user_dict = {
                        "employmentId": user_obj.get("employmentId"),
                        "gender": user_obj.get("gender"),
                        "fullName": user_obj.get("fullName"),
                        "noteId": note_id,
                        "pinfl": user_obj.get('pinfl'),
                        "image": user_obj.get('image'),
                        "isOwner": True if pinfl == user_obj.get('pinfl') else False,
                    }
                    await uow.note_users.add_one(note_user_dict)
            await uow.commit()
            note_obj = Note(**updated_note).to_read_model_as_list()
            note_obj["usersCount"] = len(users_info)
            return note_obj

    async def get_note(self, uow: IUnitOfWork, note_id: int, pinfl: str):
        note_users = []
        note_user_obj = NoteUserService()

        async with uow:
            note = await uow.notes.find_one(note_id)
            if not note:
                raise CustomHTTPException(status_code=404, detail="note has not found")
            note_users = await note_user_obj.get_note_users(uow, note_id)
            isOwner = False
            users = []
            for user in note_users:
                user_detail = dict(user)
                if user_detail.get('isOwner') and user_detail.get('pinfl') == pinfl:
                    isOwner = True
                if user_detail.get('gender') and user_detail.get('gender') == 'F':
                    user_detail['image'] = None
                user_detail.pop('pinfl')
                user_detail.pop('gender')
                users.append(user_detail)
            note['isOwner'] = isOwner

        note_with_users = {**note, "users": users}
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
    
    async def get_employments(self, organization_id: int, pinfl: str, search: str):
        state_client = StateClient()
        employments_info = await state_client.get_employments(
            organization_id=organization_id,
            pinfl=pinfl,
            search=search
        )
        return employments_info




class NoteUserService:
    async def get_note_users(self, uow: IUnitOfWork, note_id: int):
        async with uow:
            note_users = await uow.note_users.find_all(note_id=note_id)
            return note_users