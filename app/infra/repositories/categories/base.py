from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.entities.categories import Category


@dataclass
class BaseCategoriesRepository(ABC):
    @abstractmethod
    async def check_category_exists_by_title(self, title: str) -> bool:
        ...

    @abstractmethod
    async def add_category(self, category: Category) -> None:
        ...
