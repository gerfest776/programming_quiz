from typing import Any

from pydantic import BaseSettings, PostgresDsn, validator


class AppSettings(BaseSettings):
    API_PREFIX: str


class DatabaseSettings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str | int
    DATABASE_NAME: str
    ASYNC_DATABASE_URI: str | None

    @validator("ASYNC_DATABASE_URI", pre=True)
    def assemble_db_connection(
        self, v: str | None, values: dict[str, Any]
    ) -> Any:
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
    pass


class MainConfig(BaseSettings):
    db: DatabaseSettings = DatabaseSettings(_env_file=".env")
    redis: RedisSettings = RedisSettings(_env_file=".env")
    app: AppSettings = AppSettings(_env_file=".env")


def get_config() -> MainConfig:
    return MainConfig(_env_file=".env", _env_file_encoding="utf-8")
