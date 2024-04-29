from src.usecase.schemas.notes import NoteSchema, NoteSchemaAdd, NoteSchemaEdit
from src.usecase.utils.repository import AbstractRepository
from src.usecase.utils.unitofwork import IUnitOfWork


class NotesService:
    async def add_note(self, uow: IUnitOfWork, note: NoteSchemaAdd):
        notes_dict = note.model_dump()
        user_ids = notes_dict.pop('Users')
        notes_dict.update({'OrganizationId': 1})
        note_users = []
        async with uow:
            note = await uow.notes.add_one(notes_dict)
            for user_id in user_ids:
                note_user_dict = {
                    'UserId': user_id,
                    'Fullname': 'Dilshod Bakhtiyorov',
                    'NoteId': note.get('Id')
                }
                note_user = await uow.note_users.add_one(note_user_dict)
                note_users.append(note_user)
            await uow.commit()
            note.update({'Users': note_users})
            return note

    async def get_notes(self, uow: IUnitOfWork):
        async with uow:
            tasks = await uow.notes.find_all()
            return tasks

    async def edit_note(self, uow: IUnitOfWork, note_id: int, note: NoteSchemaEdit):
        notes_dict = note.model_dump()
        async with uow:
            await uow.notes.edit_one(note_id, notes_dict)
            await uow.commit()