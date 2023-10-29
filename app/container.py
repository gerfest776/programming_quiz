from dependency_injector import containers, providers
from dotenv import load_dotenv

from app.infrastructure.db.models.base import SqlAlchemyDatabase

load_dotenv()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(yaml_files=["./app/config.yml"])

    db = providers.Singleton(
        SqlAlchemyDatabase,
        host=config.database.host,
        port=config.database.port,
        name=config.database.name,
        user=config.database.user,
        password=config.database.password,
    )
