from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass

from infra.repositories.filters.base import GetFilters
from domain.entities.categories import Category


@dataclass
class BaseCategoriesRepository(ABC):
    @abstractmethod
    async def check_category_exists_by_title(self, title: str) -> bool:
        ...

    @abstractmethod
    async def add_category(self, category: Category) -> None:
        ...

    @abstractmethod
    async def get_categories(
        self, filters: GetFilters
    ) -> tuple[Iterable[Category], int]:
        ...
