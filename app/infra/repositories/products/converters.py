from typing import Any
from domain.entities.products import Product


def convert_product_entity_to_document(product: Product) -> dict[str, Any]:
    return {
        'oid': product.oid,
        'title': product.title.as_generic_type(),
        'created_at': product.created_at,
        'description': product.description.as_generic_type(),
        'price': product.price.as_generic_type(),
        'image_oid': product.image_oid,
        'category_oid': product.category_oid,
        'characteristics': {
            title.as_generic_type(): value
            for title, value in product.characteristics.items()
        },
    }