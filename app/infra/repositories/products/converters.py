from typing import Any
from domain.values.products import CharacteristicTitle, Description, Price, ProductTitle
from infra.models.products import Products
from infra.repositories.converters import model_to_document
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


def convert_product_model_to_entity(product_model: Products) -> Product:
    product_document = model_to_document(product_model)

    return Product(
        oid=product_document["oid"],
        title=ProductTitle(value=product_document["title"]),
        created_at=product_document["created_at"],
        description=Description(product_document["description"]),
        price=Price(product_document["price"]),
        image_oid=product_document["image_oid"],
        category_oid=product_document["category_oid"],
        characteristics={
            CharacteristicTitle(title): value
            for title, value in product_document["characteristics"].items()
        },
    )
