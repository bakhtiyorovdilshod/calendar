from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query

from src.usecase.utils.user import User, get_current_user
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
    uow: UOWDep,
    user: User = Depends(get_current_user)
):
    note = await NotesService().add_note(uow, note, user.last_organization_id)
    return note


@router.get("")
async def get_notes(
    uow: UOWDep,
    user: User = Depends(get_current_user),
    begin_date: datetime = Query(..., description="Start date for filtering notes", format="date-time"),
    end_date: datetime = Query(..., description="End date for filtering notes", format="date-time"),
):
    """
    Retrieve notes filtered by date range.
    """
    notes = await NotesService().get_notes(uow, begin_date, end_date)
    return notes

@router.get("/{note_id}")
async def get_single_note(
    note_id: int,
    uow: UOWDep,
    user: User = Depends(get_current_user)
):
    """
    Retrieve a single note by its ID.
    """
    note = await NotesService().get_note(uow, note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}")
async def edit_note(
    note_id: int,
    note: NoteSchemaEdit,
    uow: UOWDep,
    user: User = Depends(get_current_user)
):
    """
    Retrieve a single note by its ID.
    """
    note = await NotesService().edit_note(uow, note_id, note)
    if note is None:
        raise HTTPException(status_code=404, detail="dddds not found")
    return note
