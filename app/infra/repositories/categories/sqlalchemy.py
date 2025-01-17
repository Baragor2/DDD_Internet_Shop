from collections.abc import Iterable
from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import delete, insert, select, update

from domain.values.categories import CategoryTitle
from infra.repositories.filters.base import GetFilters
from domain.entities.categories import Category
from infra.models.categories import Categories
from infra.repositories.categories.base import BaseCategoriesRepository

from sqlalchemy.ext.asyncio import AsyncSession

from infra.repositories.categories.converters import convert_category_model_to_entity, convert_category_entity_to_document


@dataclass
class SqlAlchemyCategoriesRepository(BaseCategoriesRepository):
    session: AsyncSession

    async def check_category_exists_by_title(self, title: CategoryTitle) -> bool:
        query = select(Categories).where(Categories.title == title.as_generic_type())
        result = await self.session.execute(query)
        return bool(result.scalar_one_or_none())

    async def check_category_exists_by_oid(self, oid: UUID) -> bool:
        query = select(Categories).where(Categories.oid == oid)
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
    
    async def delete_category_by_title(self, title: CategoryTitle) -> None:
        query = delete(Categories).where(Categories.title == title.as_generic_type())
        await self.session.execute(query)

    async def update_category_title(
        self, 
        old_title: CategoryTitle, 
        new_title: CategoryTitle
    ) -> Category:
        update_query = (
            update(Categories).
            where(Categories.title == old_title.as_generic_type()).
            values(title=new_title.as_generic_type())
        )
        await self.session.execute(update_query)

        select_query = select(Categories).where(Categories.title == new_title.as_generic_type())
        updated_category = await self.session.execute(select_query)

        return convert_category_model_to_entity(updated_category.scalar_one_or_none())
