from dataclasses import dataclass

from sqlalchemy import insert, select

from domain.entities.categories import Category
from infra.models.categories import Categories
from infra.repositories.categories.base import BaseCategoriesRepository

from sqlalchemy.ext.asyncio import AsyncSession

from infra.repositories.categories.converters import convert_category_entity_to_document


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