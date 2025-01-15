from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.products import Product


@dataclass
class BaseProductsRepository(ABC):
    @abstractmethod
    async def get_all_products(self, limit: int, offset: int) -> Iterable[Product]:
        ...

    @abstractmethod
    async def get_product_by_oid(self, oid: str) -> Product | None:
        ...

    @abstractmethod
    async def add_product(self, product: Product) -> None:
        ...
