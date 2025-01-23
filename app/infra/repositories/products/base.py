from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass

from application.api.filters import GetFilters
from domain.values.products import ProductTitle
from domain.entities.products import Product


@dataclass
class BaseProductsRepository(ABC):
    @abstractmethod
    async def check_product_exists_by_title(self, title: ProductTitle) -> bool:
        ...

    @abstractmethod
    async def add_product(self, product: Product) -> None:
        ...

    @abstractmethod
    async def get_products(self, filters: GetFilters) -> tuple[Iterable[Product], int]:
        ...
