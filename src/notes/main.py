from fastapi import FastAPI
from sqladmin import Admin

from notes.core.db import engine
from notes.api.routers import main_router
from notes.core.config import settings
from notes.admin.views import UserAdmin, NoteAdmin, CategoryAdmin


app = FastAPI(title=settings.APP_TITLE, description=settings.DESCRIPTION)

app.include_router(main_router)

admin = Admin(app=app, engine=engine)

admin.add_view(UserAdmin)
admin.add_view(NoteAdmin)
admin.add_view(CategoryAdmin)
