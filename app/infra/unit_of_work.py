from dataclasses import dataclass
from typing import Callable
from infra.repositories.categories.sqlalchemy import SqlAlchemyCategoryRepository

from sqlalchemy.ext.asyncio import AsyncSession

@dataclass
class UnitOfWork:
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

    def get_categories_repository(self) -> SqlAlchemyCategoryRepository:
        return SqlAlchemyCategoryRepository(self.session)