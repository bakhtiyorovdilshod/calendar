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
    createdAt = Column(TIMESTAMP, default=func.now())
    updatedAt = Column(TIMESTAMP, nullable=True)

    def to_read_model_as_list(self) -> NoteSchemaList:
        return NoteSchemaList(
            id=self.id,
            title=self.title,
            fromTime=self.fromTime.strftime("%H:%M"),
            tillTime=self.tillTime.strftime("%H:%M"),
            colorCode=self.colorCode,
        )

    def to_read_model_as_detail(self) -> NoteSchemaDetail:
        return NoteSchemaDetail(
            id=self.id,
            title=self.title,
            date=self.date,
            fromTime=self.fromTime.strftime("%H:%M"),
            tillTime=self.tillTime.strftime("%H:%M"),
            location=self.location,
            description=self.description,
            colorCode=self.colorCode,
            createdAt=self.createdAt.date().strftime("%Y-%m-%d"),
        )


class NoteUser(Base):
    """NoteUser is a SQLAlchemy model representing a note-user relationship."""

    __tablename__ = "note_users"

    id = Column(Integer, primary_key=True)
    userId = Column(Integer)
    fullName = Column(String)
    noteId = Column(Integer, ForeignKey("notes.id"))
    createdAt = Column(TIMESTAMP, default=func.now())
    updatedAt = Column(TIMESTAMP, nullable=True)
    isOwner = Column(Boolean, default=False)
    isDelete = Column(Boolean, default=False)

    def to_read_model_as_list(self) -> NoteUserSchemaList:
        return NoteUserSchemaList(
            id=self.id, userId=self.userId, fullName=self.fullName, isOwner=self.isOwner
        )
