from dataclasses import dataclass
from typing import Callable
from infra.repositories.carts.sqlalchemy import SqlAlchemyCartsRepository
from infra.repositories.users.sqlalchemy import SqlAlchemyUsersRepository
from infra.repositories.products.sqlalchemy import SqlAlchemyProductsRepository
from infra.repositories.categories.sqlalchemy import SqlAlchemyCategoriesRepository

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SQLAlchemyUnitOfWork:
    session_factory: Callable[[], AsyncSession]
    session: AsyncSession = None

    async def __aenter__(self):
        self.session = self.session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            await self.session.commit()
        else:
            await self.session.rollback()
        await self.session.close()

    async def get_categories_repository(self) -> SqlAlchemyCategoriesRepository:
        return SqlAlchemyCategoriesRepository(self.session)

    async def get_products_repository(self) -> SqlAlchemyProductsRepository:
        return SqlAlchemyProductsRepository(self.session)

    async def get_users_repository(self) -> SqlAlchemyUsersRepository:
        return SqlAlchemyUsersRepository(self.session)

    async def get_carts_repository(self) -> SqlAlchemyCartsRepository:
        return SqlAlchemyCartsRepository(self.session)
