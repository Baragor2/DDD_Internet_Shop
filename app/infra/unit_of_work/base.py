from abc import ABC, abstractmethod
from dataclasses import dataclass

from infra.repositories.carts.base import BaseCartsRepository
from infra.repositories.categories.base import BaseCategoriesRepository
from infra.repositories.products.base import BaseProductsRepository
from infra.repositories.users.base import BaseUsersRepository


@dataclass
class UnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        ...

    @abstractmethod
    async def get_categories_repository(self) -> BaseCategoriesRepository:
        ...

    @abstractmethod
    async def get_products_repository(self) -> BaseProductsRepository:
        ...

    @abstractmethod
    async def get_users_repository(self) -> BaseUsersRepository:
        ...

    @abstractmethod
    async def get_carts_repository(self) -> BaseCartsRepository:
        ...
