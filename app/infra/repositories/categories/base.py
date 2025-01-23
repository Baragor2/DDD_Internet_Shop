from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from domain.values.categories import CategoryTitle
from infra.repositories.filters.base import GetFilters
from domain.entities.categories import Category


@dataclass
class BaseCategoriesRepository(ABC):
    @abstractmethod
    async def check_category_exists_by_title(self, title: CategoryTitle) -> bool:
        ...

    @abstractmethod
    async def check_category_exists_by_oid(self, oid: UUID) -> bool:
        ...

    @abstractmethod
    async def add_category(self, category: Category) -> None:
        ...

    @abstractmethod
    async def get_categories(
        self, filters: GetFilters
    ) -> tuple[Iterable[Category], int]:
        ...

    @abstractmethod
    async def delete_category_by_title(self, title: CategoryTitle) -> None:
        ...

    @abstractmethod
    async def update_category_title(
        self, old_title: CategoryTitle, new_title: CategoryTitle
    ) -> Category:
        ...
