from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from notes.core.base import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    pass
