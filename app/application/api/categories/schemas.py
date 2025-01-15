from datetime import datetime
from pydantic import BaseModel

from app.domain.entities.categories import Category


class CreateCategoryRequestSchema(BaseModel):
    title: str


class CreateCategoryResponseSchema(BaseModel):
    oid: str
    created_at: datetime
    title: str

    @classmethod
    def from_entity(cls, category: Category) -> 'CreateCategoryResponseSchema':
        return cls(
            oid=category.oid,
            created_at=category.created_at,
            title=category.title.as_generic_type(),
        )
