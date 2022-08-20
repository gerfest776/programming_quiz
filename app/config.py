from pydantic import BaseSettings


class AppSettings(BaseSettings):
    pass


class DatabaseSettings(BaseSettings):
    pass


class RedisSettings(BaseSettings):
    pass


class MainConfig(BaseSettings):
    pass


def get_config() -> MainConfig:
    return MainConfig(
        _env_file=".env",
        _env_file_encoding="utf-8"
    )
