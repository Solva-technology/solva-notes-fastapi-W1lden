from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from notes.api.schemas.note import NoteCreate, NoteDB, NoteUpdate
from notes.api.validators import check_note_exist
from notes.core.db import get_async_session
from notes.core.user import current_user
from notes.db.crud.note import note_crud

router = APIRouter()


# POST
@router.post("/", response_model=NoteDB)
async def create_new_note(
    new_note: NoteCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    data = new_note.dict(exclude={"category_ids"})
    return await note_crud.create_with_categories(
        obj_in={**data, "user_id": user.id},
        category_ids=new_note.category_ids,
        session=session,
    )


# PATCH
@router.patch("/{id}/update", response_model=NoteDB)
async def update_note(
    id: int,
    note_in: NoteUpdate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    db_note = await check_note_exist(note_id=id, session=session, user=user)

    obj_in = note_in.dict(exclude_unset=True)
    return await note_crud.update_with_categories(
        db_obj=db_note, obj_in=obj_in, session=session
    )


# GET
@router.get("/all", response_model=list[NoteDB])
async def get_all_notes(
    session: AsyncSession = Depends(get_async_session), user=Depends(current_user)
):
    return await note_crud.get_multi_filtered(session=session, user=user)


@router.get("/{id}", response_model=NoteDB)
async def get_note_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    await check_note_exist(note_id=id, session=session, user=user)
    note = await note_crud.get_by_id_filtered(id, session=session, user=user)
    if not note:
        raise HTTPException(
            status_code=404, detail="Заметка не найдена или доступ запрещен!"
        )

    return note


# DELETE
@router.delete("/{id}/delete", status_code=204)
async def delete_note(
    id: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    note = await note_crud.get_by_id_filtered(note_id=id, session=session, user=user)
    if not note:
        raise HTTPException(status_code=404, detail="Заметка не найдена!")
    await session.delete(note)
    await session.commit()
