from typing import Union

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users import (
    FastAPIUsers, BaseUserManager, IntegerIDMixin, InvalidPasswordException
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from fastapi_users.authentication import (
    BearerTransport, JWTStrategy, AuthenticationBackend
)

from notes.core.db import get_async_session
from notes.core.config import settings
from notes.db.models import User

from notes.api.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_WORD, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


class UserManager(IntegerIDMixin, BaseUserManager):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User]
    ) -> None:
        if len(password) <= 7:
            raise InvalidPasswordException(
                reason='Пароль должен соответвовать крутым нормам'
            )

        if user.email in password:
            raise InvalidPasswordException(
                reason='Пароль не должен содержать вашего email-а'
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
