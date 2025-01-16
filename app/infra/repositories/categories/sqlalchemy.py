from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy import delete, insert, select

from infra.repositories.filters.base import GetFilters
from domain.entities.categories import Category
from infra.models.categories import Categories
from infra.repositories.categories.base import BaseCategoriesRepository

from sqlalchemy.ext.asyncio import AsyncSession

from infra.repositories.categories.converters import convert_category_model_to_entity, convert_category_entity_to_document


@dataclass
class SqlAlchemyCategoryRepository(BaseCategoriesRepository):
    session: AsyncSession

    async def check_category_exists_by_title(self, title: str) -> bool:
        query = select(Categories).where(Categories.title == title)
        result = await self.session.execute(query)
        return bool(result.scalar_one_or_none())

    async def add_category(self, category: Category) -> None:
        query = insert(Categories).values(
            convert_category_entity_to_document(category)
        )
        await self.session.execute(query)

    async def get_categories(self, filters: GetFilters) -> tuple[Iterable[Category], int]:
        query = select(Categories).limit(filters.limit).offset(filters.offset)
        result = await self.session.execute(query)

        categories = [
            convert_category_model_to_entity(category_model=category_model[0])
            for category_model in result.all()
        ]

        return categories, len(categories)
    
    async def delete_category_by_title(self, title: str) -> None:
        query = delete(Categories).where(Categories.title == title)
        await self.session.execute(query)
