from notes.db.crud.base import CRUDBase
from notes.db.models import Category


class CRUDCategory(CRUDBase):
    pass


category_crud = CRUDCategory(Category)
