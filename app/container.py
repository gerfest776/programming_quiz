from dependency_injector import containers, providers
from dotenv import load_dotenv

from app.infrastructure.db.base import AsyncDatabase

load_dotenv()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["./app/config.yml"])

    db_uri = providers.Factory(
        lambda c: f"postgresql+asyncpg://{c.database.user}:{c.database.password}"
        f"@{c.database.host}:{c.database.port}/{c.database.db_name}",
        c=config
    )

    db = providers.Singleton(
        AsyncDatabase,
        db_url=db_uri
    )


