from dataclasses import dataclass

from sqlalchemy import insert

from domain.entities.carts import Cart
from infra.models.carts import Carts
from infra.repositories.carts.base import BaseCartsRepository
from infra.repositories.carts.converters import convert_cart_entity_to_document

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SqlAlchemyCartsRepository(BaseCartsRepository):
    session: AsyncSession

    async def add_cart(self, cart: Cart) -> None:
        query = insert(Carts).values(
            convert_cart_entity_to_document(cart)
        )
        await self.session.execute(query)
