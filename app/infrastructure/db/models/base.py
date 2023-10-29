from sqlalchemy.orm import DeclarativeBase


class SqlAlchemyDatabase:
    DRIVER = 'postgresql+asyncpg'

    def __init__(
            self,
            *,
            host: str,
            port: str,
            name: str,
            user: str,
            password: str
    ):
        self.db_uri = f'{self.DRIVER}://{user}:{password}@{host}:{port}/{name}'


class Base(DeclarativeBase):
    pass

