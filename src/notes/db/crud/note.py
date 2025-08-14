from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from notes.db.crud.base import CRUDBase
from notes.db.models import Note, Category, note_category_association


class CRUDNote(CRUDBase):
    async def create_with_categories(
        self,
        obj_in: dict,
        category_ids: list[int] | None,
        session: AsyncSession
    ):
        note = self.model(**obj_in)
        session.add(note)
        await session.flush()

        if category_ids:
            stmt = insert(note_category_association).values(
                [{"note_id": note.id, "category_id": cat_id} for cat_id in category_ids]
            )
            await session.execute(stmt)

        await session.commit()

        # Теперь безопасно подгружаем категории
        note_with_categories = await session.execute(
            select(Note)
            .options(selectinload(Note.categories))
            .where(Note.id == note.id)
        )
        note_with_categories = note_with_categories.scalars().first()

        return note_with_categories


note_crud = CRUDNote(Note)
