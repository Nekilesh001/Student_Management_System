from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_URL: str
    APP_NAME: str = "Student Management System"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
