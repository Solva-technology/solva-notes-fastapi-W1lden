from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from notes.api.validators import check_note_exist
from notes.api.schemas.note import NoteCreate, NoteDB
from notes.core.db import get_async_session
from notes.db.crud.note import note_crud

router = APIRouter()


@router.post(
    '/',
    response_model=NoteDB
)
async def create_new_note(
    new_note: NoteCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await note_crud.create(new_note, session)


@router.get(
    '/all',
    response_model=list[NoteDB]

)
async def get_all_notes(
    session: AsyncSession = Depends(get_async_session),
):
    return await note_crud.get_multi(session=session)


@router.get(
    '/{id}',
    response_model=NoteDB
)
async def get_note_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await check_note_exist(note_id=id, session=session)
