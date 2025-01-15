from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from domain.entities.categories import Category


class CreateCategoryRequestSchema(BaseModel):
    title: str


class CreateCategoryResponseSchema(BaseModel):
    oid: UUID
    created_at: datetime
    title: str

    @classmethod
    def from_entity(cls, category: Category) -> 'CreateCategoryResponseSchema':
        return cls(
            oid=category.oid,
            created_at=category.created_at,
            title=category.title.as_generic_type(),
        )
