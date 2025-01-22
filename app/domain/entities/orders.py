from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.values.products import Price


@dataclass(eq=False)
class Order(BaseEntity):
    user_oid: UUID
    total_price: Price

    @classmethod
    def create_order(
        cls,
        user_oid: UUID,
        total_price: Price,
    ) -> "Order":
        new_order = cls(
            user_oid=user_oid,
            total_price=total_price,
        )

        return new_order
