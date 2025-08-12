from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_TITLE: str
    DESCRIPTION: str

    SECRET_WORD: str = 'SECRET'
    DATABASE_URL: str
    PRODUCTION: bool

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
