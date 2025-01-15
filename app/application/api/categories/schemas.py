from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from application.api.schemas import BaseQueryResponseSchema
from domain.entities.categories import Category


class CreateCategoryRequestSchema(BaseModel):
    title: str


class CreateCategoryResponseSchema(BaseModel):
    oid: UUID
    title: str

    @classmethod
    def from_entity(cls, category: Category) -> 'CreateCategoryResponseSchema':
        return cls(
            oid=category.oid,
            title=category.title.as_generic_type(),
        )

    
class CategoryDetailSchema(BaseModel):
    oid: UUID
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, category: Category) -> 'CategoryDetailSchema':
        return cls(
            oid=category.oid,
            title=category.title.as_generic_type(),
            created_at=category.created_at,
        )


class GetCategoriesQueryResponseSchema(BaseQueryResponseSchema):
    items: list[CategoryDetailSchema]

