from dataclasses import dataclass

from sqlalchemy import insert, select

from domain.entities.products import Product
from domain.values.products import ProductTitle
from infra.models.products import Products
from infra.repositories.products.base import BaseProductsRepository

from sqlalchemy.ext.asyncio import AsyncSession

from infra.repositories.products.converters import convert_product_entity_to_document

@dataclass
class SqlAlchemyProductsRepository(BaseProductsRepository):
    session: AsyncSession

    async def check_product_exists_by_title(self, title: ProductTitle) -> bool:
        query = select(Products).where(Products.title == title.as_generic_type())
        result = await self.session.execute(query)
        return bool(result.scalar_one_or_none())

    async def add_product(self, product: Product) -> None:
        query = insert(Products).values(
            convert_product_entity_to_document(product)
        )
        await self.session.execute(query)
