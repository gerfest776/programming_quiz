from typing import Any

from pydantic import BaseSettings, PostgresDsn, validator


class AppSettings(BaseSettings):
    API_PREFIX: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 180
    SECRET_KEY: str
    ALGORITHM: str
    HOST: str
    PORT: int
    WORKERS: int


class DatabaseSettings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str | int
    DATABASE_NAME: str
    ASYNC_DATABASE_URI: str | None

    @validator("ASYNC_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=str(values.get("DATABASE_PORT")),
            path=f"/{values.get('DATABASE_NAME') or ''}",
        )


class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int | str
    REDIS_URI: str | None

    @validator("REDIS_URI", pre=True)
    def assemble_redis_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"redis://{values.get('REDIS_HOST')}:{values.get('REDIS_PORT')}"


class MainConfig(BaseSettings):
    db: DatabaseSettings = DatabaseSettings(_env_file=".env")
    redis: RedisSettings = RedisSettings(_env_file=".env")
    app: AppSettings = AppSettings(_env_file=".env")


def get_config() -> MainConfig:
    return MainConfig(_env_file=".env", _env_file_encoding="utf-8")
