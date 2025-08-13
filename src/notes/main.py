from fastapi import FastAPI

from notes.api.routers import main_router
from notes.core.config import settings

app = FastAPI(title=settings.APP_TITLE, description=settings.DESCRIPTION)

app.include_router(main_router)
