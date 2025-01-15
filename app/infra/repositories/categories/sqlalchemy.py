from dataclasses import dataclass

from sqlalchemy import insert, select

from app.domain.entities.categories import Category
from app.infra.models.categories import Categories
from app.infra.repositories.categories.base import BaseCategoriesRepository

from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.repositories.categories.converters import convert_category_entity_to_document


@dataclass
class SqlAlchemyCategoryRepository(BaseCategoriesRepository):
    async def check_category_exists_by_title(self, session: AsyncSession, title: str) -> bool:
        query = select(Categories).where(
            title=title,
        )
        result = await session.execute(query)
        return bool(result.scalar_one_or_none())
        
    async def add_category(self, session: AsyncSession, category: Category) -> None:
        query = insert(Categories).values(
            convert_category_entity_to_document(category)
        )
        await session.execute(query)