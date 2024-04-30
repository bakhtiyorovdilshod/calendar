from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional, List


class NoteSchema(BaseModel):
    """NoteSchema represents the schema of a Note."""

    id: Optional[int]
    organization_id: Optional[int]
    title: Optional[str]
    date: Optional[date]
    from_time: Optional[time]
    till_time: Optional[time]
    location: Optional[str]
    description: Optional[str]
    color_code: Optional[str]
    is_delete: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]



class NoteSchemaAdd(BaseModel):
    Title: str
    Date: date
    FromTime: time
    TillTime: time
    Location: str
    Description: str
    ColorCode: str
    UserIds: List[int]

class NoteSchemaList(BaseModel):
    Id: int
    Title: str
    FromTime: time
    TillTime: time
    ColorCode: str

class NoteUserSchemaList(BaseModel):
    Id: int
    UserId: int
    Fullname: str
    IsOwner: bool


class NoteSchemaDetail(BaseModel):
    Id: int
    Title: str
    Date: date
    FromTime: time
    TillTime: time
    Location: str
    Description: str
    ColorCode: str
    CreatedAt: datetime

class NoteSchemaAddResponse(BaseModel):
    Id: int
    # OrganizationId: int
    # Title: str
    # Date: date
    # FromTime: time
    # TillTime: time
    # Location: str
    # Description: str
    # ColorCode: str
    # CreatedAt: date



class NoteSchemaEdit(BaseModel):
    Title: str
    Date: date
    FromTime: time
    TillTime: time
    Location: str
    Description: str
    ColorCode: str
    UserIds: List[int]
