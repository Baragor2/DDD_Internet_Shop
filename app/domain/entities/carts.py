from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass(eq=False)
class Cart(BaseEntity):
    @classmethod
    def create_cart(cls) -> "Cart":
        new_cart = cls()
        return new_cart
