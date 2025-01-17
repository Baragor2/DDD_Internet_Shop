from abc import ABC, abstractmethod
from dataclasses import dataclass

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
