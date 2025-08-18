from fastapi import FastAPI
from sqladmin import Admin

from notes.core.db import engine
from notes.admin.auth import AdminAuth
from notes.api.routers import main_router
from notes.core.config import settings
from notes.admin.views import UserAdmin, NoteAdmin, CategoryAdmin


app = FastAPI(title=settings.APP_TITLE, description=settings.DESCRIPTION)

app.include_router(main_router)

auth_backend = AdminAuth(secret_key=f"{settings.ADMIN}")
admin = Admin(app=app, engine=engine, authentication_backend=auth_backend)

admin.add_view(UserAdmin)
admin.add_view(NoteAdmin)
admin.add_view(CategoryAdmin)
