import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str

    POSTGRES_DB_TEST: str
    POSTGRES_USER_TEST: str
    POSTGRES_HOST_TEST: str
    POSTGRES_PORT_TEST: str
    POSTGRES_PASSWORD_TEST: str

    TEST: bool

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_db_url():
    return (f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")


def get_test_db_url():
    return (f"postgresql+asyncpg://{settings.POSTGRES_USER_TEST}:{settings.POSTGRES_PASSWORD_TEST}@"
            f"{settings.POSTGRES_HOST_TEST}:{settings.POSTGRES_PORT_TEST}/{settings.POSTGRES_DB_TEST}")


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}
