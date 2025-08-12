from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from notes.api.validators import check_category_exist
from notes.api.schemas.category import CategoryCreate, CategoryDB
from notes.core.db import get_async_session
from notes.db.crud.category import category_crud

router = APIRouter()


@router.post(
    '/',
    response_model=CategoryDB
)
async def create_new_category(
    new_category: CategoryCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await category_crud.create(new_category, session)


@router.get(
    '/all',
    response_model=list[CategoryDB]

)
async def get_all_categories(
    session: AsyncSession = Depends(get_async_session),
):
    return await category_crud.get_multi(session=session)


@router.get(
    '/{id}',
    response_model=CategoryDB
)
async def get_category_by_id(
    id: int,
    session: AsyncSession = Depends(get_async_session),
):
    return await check_category_exist(category_id=id, session=session)
