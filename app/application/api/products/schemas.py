from decimal import Decimal
from typing import Any
from uuid import UUID
from pydantic import BaseModel

from domain.entities.products import Product


class CreateProductRequestSchema(BaseModel):
    title: str
    description: str
    price: Decimal
    category_oid: UUID
    characteristics: dict[str, Any]


class CreateProductResponseSchema(BaseModel):
    oid: UUID
    title: str
    description: str
    price: Decimal
    image_oid: UUID | None
    category_oid: UUID
    characteristics: dict[str, Any]

    @classmethod
    def from_entity(cls, product: Product) -> 'CreateProductResponseSchema':
        return cls(
            oid=product.oid,
            title=product.title.as_generic_type(),
            description=product.description.as_generic_type(),
            price=product.price.as_generic_type(),
            image_oid=product.image_oid,
            category_oid=product.category_oid,
            characteristics={
                title.as_generic_type(): value
                for title, value in product.characteristics.items()
            },
        )