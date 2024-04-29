from fastapi import APIRouter
from .dependencies import *
from src.usecase.schemas.notes import NoteSchema, NoteSchemaAdd, NoteSchemaAddResponse, NoteSchemaEdit
from src.usecase.services.notes import NotesService

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post("")
async def add_note(
    note: NoteSchemaAdd,
    uow: UOWDep
):
    note = await NotesService().add_note(uow, note)
    # print(note.get('created_at'))
    # response = NoteSchemaAddResponse(
    #     Id=note.get('id'),
    #     OrganizationId=note.get('organization_id'),
    #     Description=note.get('description'),
    #     Title=note.get('title'),
    #     Date=note.get('date'),
    #     FromTime=note.get('from_time'),
    #     TillTime=note.get('till_time'),
    #     Location=note.get('location'),
    #     ColorCode=note.get('color_code'),
    #     CreatedAt=note.get('created_at')
    # )
    return note


@router.get("")
async def get_notes(
    uow: UOWDep,
):
    users = await NotesService().get_notes(uow)
    return users