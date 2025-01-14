from dataclasses import dataclass, field
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.values.cart_items import Quantity


@dataclass(eq=False)
class CartItem(BaseEntity):
    cart_oid: UUID
    order_oid: UUID | None = field(
        default=None,
        kw_only=True,
    )
    product_oid: UUID
    quantity: Quantity 

    @classmethod
    def create_cart_item(
        cls, 
        cart_oid: UUID,
        order_oid: UUID,
        product_oid: UUID, 
        quantity: Quantity,
    ) -> 'CartItem':
        new_cart_item = cls(
            cart_oid=cart_oid,
            order_oid=order_oid,
            product_oid=product_oid,
            quantity=quantity,
        ) 
        return new_cart_item
   