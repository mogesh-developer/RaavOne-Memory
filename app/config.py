from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "RaavOne Memory"
    DATABASE_URL: str = "sqlite:///./storage/memory.db"


settings = Settings()