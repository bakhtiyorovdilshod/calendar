from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Time, Text, Boolean, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from src.infrastructure.postgres.database import Base
from src.usecase.schemas.notes import NoteSchemaDetail, NoteSchemaList, NoteUserSchemaList

class Note(Base):
    """Note is a SQLAlchemy model representing a note entity."""

    __tablename__ = "notes"
    
    Id = Column(Integer, primary_key=True)
    OrganizationId = Column(Integer)
    Title = Column(String)
    Date = Column(Date)
    FromTime = Column(Time)
    TillTime = Column(Time)
    Location = Column(String)
    Description = Column(Text)
    ColorCode = Column(String)
    IsDelete = Column(Boolean, default=False)
    CreatedAt = Column(TIMESTAMP, default=func.now())
    UpdatedAt = Column(TIMESTAMP, nullable=True)

    def to_read_model_as_list(self) -> NoteSchemaList:
        return NoteSchemaList(
            Id=self.Id,
            Title=self.Title,
            FromTime=self.FromTime.strftime("%H:%M"),
            TillTime=self.TillTime.strftime("%H:%M"),
            ColorCode=self.ColorCode,
        )
    
    def to_read_model_as_detail(self) -> NoteSchemaDetail:
        return NoteSchemaDetail(
            Id=self.Id,
            Title=self.Title,
            Date=self.Date,
            FromTime=self.FromTime.strftime("%H:%M"),
            TillTime=self.TillTime.strftime("%H:%M"),
            Location=self.Location,
            Description=self.Description,
            ColorCode=self.ColorCode,
            CreatedAt=self.CreatedAt.date().strftime("%Y-%m-%d"),
        )

class NoteUser(Base):
    """NoteUser is a SQLAlchemy model representing a note-user relationship."""
    
    __tablename__ = "note_users"

    Id = Column(Integer, primary_key=True)
    UserId = Column(Integer)
    Fullname = Column(String)
    NoteId = Column(Integer, ForeignKey('notes.Id'))
    CreatedAt = Column(TIMESTAMP, default=func.now())
    UpdatedAt = Column(TIMESTAMP, nullable=True)
    IsOwner = Column(Boolean, default=False)
    IsDelete = Column(Boolean, default=False)


    def to_read_model_as_list(self) -> NoteUserSchemaList:
        return NoteUserSchemaList(
            Id=self.Id,
            UserId=self.UserId,
            Fullname=self.Fullname,
            IsOwner=self.IsOwner
        )