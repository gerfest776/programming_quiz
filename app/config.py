from pydantic import BaseSettings


class AppSettings(BaseSettings):
    pass


class DatabaseSettings(BaseSettings):
    dsn: str

    class Config:
        env_prefix = "database_"


class RedisSettings(BaseSettings):
    pass


class MainConfig(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    app: AppSettings = AppSettings()


def get_config() -> MainConfig:
    return MainConfig(_env_file=".env", _env_file_encoding="utf-8")
