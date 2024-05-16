from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from src.app.error import CustomHTTPException
from src.usecase.schemas.notes import (
    NoteSchema,
    NoteSchemaAdd,
    NoteSchemaAddResponse,
    NoteSchemaEdit,
)
from src.usecase.services.notes import NotesService
from src.usecase.utils.user import User, get_current_user

from .dependencies import *

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


@router.post("/")
async def add_note(
    note: NoteSchemaAdd, uow: UOWDep, user: User = Depends(get_current_user)
):
    note = await NotesService().add_note(uow, note, user.last_organization_id, user.pinfl)
    return note


@router.get("/")
async def get_notes(
    uow: UOWDep,
    user: User = Depends(get_current_user),
    beginDate: datetime = Query(
        ..., description="Start date for filtering notes", format="date-time"
    ),
    endDate: datetime = Query(
        ..., description="End date for filtering notes", format="date-time"
    ),
):
    """
    Retrieve notes filtered by date range.
    """
    notes = await NotesService().get_notes(
        uow=uow,
        organization_id=user.last_organization_id,
        begin_date=beginDate,
        end_date=endDate,
        pinfl=user.pinfl,
    )
    return notes


@router.get("/{note_id}/")
async def get_single_note(
    note_id: int, uow: UOWDep, user: User = Depends(get_current_user)
):
    """
    Retrieve a single note by its ID.
    """
    print(user.pinfl)
    note = await NotesService().get_note(uow, note_id, user.pinfl)
    return note


@router.put("/{note_id}/")
async def edit_note(
    note_id: int,
    note: NoteSchemaEdit,
    uow: UOWDep,
    user: User = Depends(get_current_user),
):
    """
    Retrieve a single note by its ID.
    """
    note = await NotesService().edit_note(uow, note_id, note, user.last_organization_id, user.pinfl)
    return note


@router.delete("/{note_id}/")
async def delete_note(
    note_id: int,
    uow: UOWDep,
    user: User = Depends(get_current_user),
):
    """
    Delete a single note by its ID.
    """
    note = await NotesService().delete_note(uow, note_id)
    return note
