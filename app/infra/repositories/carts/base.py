from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.carts import Cart


@dataclass
class BaseCartsRepository(ABC):
    @abstractmethod
    async def add_cart(self, cart: Cart) -> None:
        ...
