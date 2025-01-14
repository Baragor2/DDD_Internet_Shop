from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.entities.cart_items import CartItem
from domain.values.products import Price
from domain.values.users import UserName


@dataclass(eq=False)
class Cart(BaseEntity):
    user_oid: UUID 

    @classmethod
    def create_cart(cls, user_oid: UUID) -> 'Cart':
        new_cart = cls(user_oid=user_oid)
        return new_cart
