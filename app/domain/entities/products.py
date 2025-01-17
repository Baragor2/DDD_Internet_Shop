from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.values.products import CharacteristicTitle, Description, Price, ProductTitle


@dataclass(eq=False)
class Characteristic:
    title: CharacteristicTitle
    value: Any

    @classmethod
    def create_characteristic(
        cls, 
        title: CharacteristicTitle, 
        value: Any,
    ) -> 'Characteristic':
        new_characteristic = cls(
            title=title,
            value=value,
        )

        return new_characteristic


@dataclass(eq=False)
class Product(BaseEntity):
    title: ProductTitle
    description: Description
    price: Price
    image_oid: UUID | None = field(
        default=None,
        kw_only=True,
    )
    category_oid: UUID
    characteristics: dict[CharacteristicTitle, Any]

    @classmethod
    def create_product(
        cls, 
        title: ProductTitle,
        description: Description,
        price: Price,
        image_oid: UUID | None,
        category_oid: UUID,
        characteristics: dict[CharacteristicTitle, Any],
    ) -> 'Product':
        
        new_product = cls(
            title=title,
            description=description,
            price=price,
            image_oid=image_oid,
            category_oid=category_oid,
            characteristics=characteristics,
        )

        return new_product
