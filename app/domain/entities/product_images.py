from dataclasses import dataclass
from uuid import UUID

from domain.entities.base import BaseEntity
from domain.values.products import Price


@dataclass(eq=False)
class ProductImage(BaseEntity):
    product_oid: UUID
    image: bytes

    @classmethod
    def create_product_image(
        cls,
        product_oid: UUID,
        image: bytes,
    ) -> "ProductImage":
        new_product_image = cls(
            product_oid=product_oid,
            image=image,
        )

        return new_product_image
