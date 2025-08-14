from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field

from notes.core.constants import TITLE_MAX_LEN
from .category import CategoryDB


class NoteCreate(BaseModel):
    title: str = Field(..., max_length=TITLE_MAX_LEN)
    text: Optional[str] = None

    category_ids: Optional[List[int]]


class NoteDB(NoteCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    categories: List[CategoryDB] = []

    class Config:
        from_attributes = True
