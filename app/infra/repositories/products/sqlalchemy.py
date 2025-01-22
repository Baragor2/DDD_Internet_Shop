from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy import insert, select

from infra.repositories.filters.base import GetFilters
from domain.entities.products import Product
from domain.values.products import ProductTitle
from infra.models.products import Products
from infra.repositories.products.base import BaseProductsRepository

from sqlalchemy.ext.asyncio import AsyncSession

from infra.repositories.products.converters import (
    convert_product_entity_to_document,
    convert_product_model_to_entity,
)


@dataclass
class SqlAlchemyProductsRepository(BaseProductsRepository):
    session: AsyncSession

    async def check_product_exists_by_title(self, title: ProductTitle) -> bool:
        query = select(Products).where(Products.title == title.as_generic_type())
        result = await self.session.execute(query)
        return bool(result.scalar_one_or_none())

    async def add_product(self, product: Product) -> None:
        query = insert(Products).values(convert_product_entity_to_document(product))
        await self.session.execute(query)

    async def get_products(self, filters: GetFilters) -> tuple[Iterable[Product], int]:
        query = select(Products).limit(filters.limit).offset(filters.offset)
        result = await self.session.execute(query)

        products = [
            convert_product_model_to_entity(product_model=product_model[0])
            for product_model in result.all()
        ]

        return products, len(products)
