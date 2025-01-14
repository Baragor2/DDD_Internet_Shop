from functools import lru_cache

from punq import Container, Scope
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    config: Config = container.resolve(Config)

    def create_engine(config: Config):
        return create_async_engine(config.postgres.connection_uri, future=True, echo=True)

    engine = create_engine(config)
    
    def create_session():
        return sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession
        )()

    container.register(AsyncSession, factory=create_session)

    return container
