from collections.abc import Iterable
from dataclasses import dataclass
from typing import Callable

from infra.unit_of_work.base import UnitOfWork
from domain.entities.products import Product
from infra.repositories.filters.base import GetFilters
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler


@dataclass(frozen=True)
class GetProductsQuery(BaseQuery):
    filters: GetFilters


@dataclass(frozen=True)
class GetProductsQueryHandler(BaseQueryHandler):
    uow_factory: Callable[[], UnitOfWork]

    async def handle(self, query: GetProductsQuery) -> Iterable[Product]:
        async with self.uow_factory() as uow:
            products_repository = await uow.get_products_repository()

            return await products_repository.get_products(
                filters=query.filters,
            )
