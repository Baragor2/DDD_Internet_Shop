from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.users import User
from domain.values.users import Email
from domain.entities.products import Product


@dataclass
class BaseUsersRepository(ABC):
    @abstractmethod
    async def check_user_exists_by_email(self, email: Email) -> bool:
        ...

    @abstractmethod
    async def add_user(self, product: Product) -> None:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: Email) -> User:
        ...
