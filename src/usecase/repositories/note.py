from src.infrastructure.postgres.node_dto import Note, NoteUser
from src.usecase.utils.repository import SQLAlchemyRepository


class NotesRepository(SQLAlchemyRepository):
    model = Note


class NoteUsersRepository(SQLAlchemyRepository):
    model = NoteUser
