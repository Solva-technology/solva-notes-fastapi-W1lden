from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean

from notes.core.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    notes: Mapped[list["Note"]] = relationship(back_populates='user')  # noqa
