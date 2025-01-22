from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable

from infra.unit_of_work.base import UnitOfWork
from domain.entities.categories import Category
from infra.repositories.filters.base import GetFilters
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetCategoriesQuery(BaseQuery):
    filters: GetFilters


@dataclass(frozen=True)
class GetCategoriesQueryHandler(BaseQueryHandler):
    uow_factory: Callable[[], UnitOfWork]

    async def handle(self, query: GetCategoriesQuery) -> Iterable[Category]:
        async with self.uow_factory() as uow:
            categories_repository = await uow.get_categories_repository()

            return await categories_repository.get_categories(
                filters=query.filters,
            )
