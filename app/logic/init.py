from functools import lru_cache

from punq import Container, Scope
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from logic.commands.products import CreateProductCommand, CreateProductCommandHandler
from logic.queries.categories import GetCategoriesQuery, GetCategoriesQueryHandler
from infra.repositories.categories.base import BaseCategoriesRepository
from infra.unit_of_work import UnitOfWork
from logic.commands.categories import ChangeCategoryTitleCommand, ChangeCategoryTitleCommandHandler, CreateCategoryCommand, CreateCategoryCommandHandler, DeleteCategoryCommand, DeleteCategoryCommandHandler
from logic.mediator.base import Mediator
from settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    config: Config = container.resolve(Config)

    engine = create_async_engine(config.postgres.connection_uri, future=True, echo=True)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

    container.register(UnitOfWork, factory=lambda: UnitOfWork(session_factory=session_factory))

    container.register(BaseCategoriesRepository, factory=lambda uow: uow.get_categories_repository())

    container.register(CreateCategoryCommandHandler, factory=lambda: CreateCategoryCommandHandler(
        uow_factory=lambda: container.resolve(UnitOfWork),
    ))
    container.register(DeleteCategoryCommandHandler, factory=lambda: DeleteCategoryCommandHandler(
        uow_factory=lambda: container.resolve(UnitOfWork),
    ))
    container.register(ChangeCategoryTitleCommandHandler, factory=lambda: ChangeCategoryTitleCommandHandler(
        uow_factory=lambda: container.resolve(UnitOfWork),
    ))
    container.register(GetCategoriesQueryHandler, factory=lambda: GetCategoriesQueryHandler(
        uow_factory=lambda: container.resolve(UnitOfWork),
    ))

    container.register(CreateProductCommandHandler, factory=lambda: CreateProductCommandHandler(
        uow_factory=lambda: container.resolve(UnitOfWork),
    ))

    def init_mediator() -> Mediator:
        mediator = Mediator()
        
        create_category_handler = container.resolve(CreateCategoryCommandHandler)
        delete_category_handler = container.resolve(DeleteCategoryCommandHandler) 
        change_category_title_handler = container.resolve(ChangeCategoryTitleCommandHandler)

        create_product_handler = container.resolve(CreateProductCommandHandler)

        mediator.register_command(
            CreateCategoryCommand,
            [create_category_handler],
        )
        mediator.register_command(
            DeleteCategoryCommand,
            [delete_category_handler],
        )
        mediator.register_command(
            ChangeCategoryTitleCommand,
            [change_category_title_handler],
        )

        mediator.register_command(
            CreateProductCommand,
            [create_product_handler],
        )

        mediator.register_query(
            GetCategoriesQuery,
            container.resolve(GetCategoriesQueryHandler),
        )
        
        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
