from fastapi import HTTPException
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

        if category_ids is not None and len(category_ids) > 0:
            # Получаем id реально существующих категорий
            existing_ids = await session.execute(
                select(Category.id).where(Category.id.in_(category_ids))
            )
            existing_ids = set(existing_ids.scalars().all())

            # Если что-то не найдено → ошибка
            missing_ids = set(category_ids) - existing_ids
            if missing_ids:
                raise HTTPException(
                    status_code=404,
                    detail=f"Категории не найдены: {sorted(missing_ids)}"
                )

            stmt = insert(note_category_association).values(
                [
                    {"note_id": note.id, "category_id": cat_id}
                    for cat_id in category_ids
                ]
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

    async def get_multi_filtered(
            self,
            session: AsyncSession,
            user
    ):
        # stmt = select(self.model)
        stmt = select(self.model).options(selectinload(self.model.categories))
        if not user.is_admin:
            stmt = stmt.where(self.model.user_id == user.id)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def get_by_id_filtered(
            self,
            note_id: int,
            session: AsyncSession,
            user
    ):
        # stmt = select(self.model).where(self.model.id == note_id)
        stmt = (
            select(self.model)
            .where(self.model.id == note_id)
            .options(selectinload(self.model.categories))
        )
        if not user.is_admin:
            stmt = stmt.where(self.model.user_id == user.id)
        result = await session.execute(stmt)
        return result.scalars().first()


note_crud = CRUDNote(Note)
