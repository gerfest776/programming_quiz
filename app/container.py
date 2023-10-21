from dependency_injector import containers, providers

from app.infrastructure.db.models.base import SqlAlchemyDatabase


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Singleton(
        SqlAlchemyDatabase,
        host=config.database.host,
        port=config.database.port,
        name=config.database.name,
        user=config.database.user,
        password=config.database.password,
    )
