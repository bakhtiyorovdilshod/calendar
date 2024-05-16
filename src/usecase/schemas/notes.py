from datetime import date, datetime, time
from typing import List, Optional

from pydantic import BaseModel


class NoteSchema(BaseModel):
    """NoteSchema represents the schema of a Note."""

    id: Optional[int]
    organizationId: Optional[int]
    title: Optional[str]
    date: Optional[date]
    fromTime: Optional[time]
    tillTime: Optional[time]
    location: Optional[str]
    description: Optional[str]
    colorCode: Optional[str]
    isDelete: Optional[bool]
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


class NoteSchemaAdd(BaseModel):
    title: str
    date: date
    fromTime: time
    tillTime: time
    location: str
    description: str
    colorCode: str
    userIds: List[str]


class NoteSchemaList(BaseModel):
    id: int
    title: str
    fromTime: time
    tillTime: time
    colorCode: str


class NoteUserSchemaList(BaseModel):
    id: int
    fullName: str
    isOwner: bool
    pinfl: Optional[str]
    image: Optional[str]


class NoteSchemaDetail(BaseModel):
    id: int
    title: str
    date: date
    fromTime: time
    tillTime: time
    location: str
    description: str
    colorCode: str


class NoteSchemaAddResponse(BaseModel):
    id: int
    # organizationId: int
    # title: str
    # date: date
    # fromTime: time
    # tillTime: time
    # location: str
    # description: str
    # colorCode: str
    # createdAt: date


class NoteSchemaEdit(BaseModel):
    title: str
    date: date
    fromTime: time
    tillTime: time
    location: str
    description: str
    colorCode: str
    userIds: List[int]
