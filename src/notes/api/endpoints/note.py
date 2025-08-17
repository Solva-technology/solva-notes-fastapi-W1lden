from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from notes.api.validators import check_note_exist
from notes.api.schemas.note import NoteCreate, NoteDB
from notes.core.db import get_async_session
from notes.core.user import current_user
from notes.db.crud.note import note_crud

router = APIRouter()


@router.post(
    '/',
    response_model=NoteDB
)
async def create_new_note(
    new_note: NoteCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user)
):
    data = new_note.dict(exclude={"category_ids"})
    return await note_crud.create_with_categories(
        # obj_in=data,
        obj_in={**data, "user_id": user.id},
        category_ids=new_note.category_ids,
        session=session
    )


@router.get(
    '/all',
    response_model=list[NoteDB]

)
async def get_all_notes(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user)
):
    return await note_crud.get_multi_filtered(session=session, user=user)


@router.get(
    '/{id}',
    response_model=NoteDB
)
async def get_note_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user)
):
    await check_note_exist(note_id=id, session=session, user=user)
    note = await note_crud.get_by_id_filtered(id, session=session, user=user)
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена или доступ запрещен!")

    return note
