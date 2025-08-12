from notes.db.crud.base import CRUDBase
from notes.db.models import Note


class CRUDNote(CRUDBase):
    pass


note_crud = CRUDBase(Note)
