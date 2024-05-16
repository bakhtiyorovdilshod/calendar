from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    Time,
    func,
    select,
)
from sqlalchemy.orm import mapped_column, relationship

from src.infrastructure.postgres.database import Base
from src.usecase.schemas.notes import (
    NoteSchemaDetail,
    NoteSchemaList,
    NoteUserSchemaList,
)


class Note(Base):
    """Note is a SQLAlchemy model representing a note entity."""

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    organizationId = Column(Integer)
    title = Column(String)
    date = Column(Date)
    fromTime = Column(Time)
    tillTime = Column(Time)
    location = Column(String)
    description = Column(Text)
    colorCode = Column(String)
    isDelete = Column(Boolean, default=False)
    ownerId = Column(String)
    createdAt = Column(TIMESTAMP, default=func.now())
    updatedAt = Column(TIMESTAMP, nullable=True)

    def to_read_model_as_list(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "fromTime": self.fromTime.strftime("%H:%M"),
            "tillTime": self.tillTime.strftime("%H:%M"),
            "date": self.date,
            "colorCode": self.colorCode
        }

    def to_read_model_as_detail(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date,
            "fromTime": self.fromTime.strftime("%H:%M"),
            "tillTime": self.tillTime.strftime("%H:%M"),
            "location": self.location,
            "description": self.description,
            "colorCode": self.colorCode,
            "ownerId": self.ownerId
        }


class NoteUser(Base):
    """NoteUser is a SQLAlchemy model representing a note-user relationship."""

    __tablename__ = "note_users"

    id = Column(Integer, primary_key=True)
    userId = Column(Integer, nullable=True)
    fullName = Column(String)
    pinfl = Column(String, nullable=True)
    image = Column(String, nullable=True)
    noteId = Column(Integer, ForeignKey("notes.id"))
    createdAt = Column(TIMESTAMP, default=func.now())
    updatedAt = Column(TIMESTAMP, nullable=True)
    isOwner = Column(Boolean, default=False)
    isDelete = Column(Boolean, default=False)

    def to_read_model_as_list(self) -> NoteUserSchemaList:
        return NoteUserSchemaList(
            id=self.id, 
            fullName=self.fullName, 
            isOwner=self.isOwner, 
            pinfl=self.pinfl, 
            image=self.image
        )
    
    def to_return_note_ids(self) -> list:
        return self.noteId
