from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.values.categories import CategoryTitle


@dataclass(eq=False)
class Category(BaseEntity):
    title: CategoryTitle

    @classmethod
    def create_category(cls, title: CategoryTitle) -> 'Category':
        new_category = cls(title=title)
        return new_category