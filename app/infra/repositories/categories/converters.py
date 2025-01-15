from infra.repositories.converters import model_to_document
from infra.models.categories import Categories
from domain.values.categories import CategoryTitle
from domain.entities.categories import Category


def convert_category_entity_to_document(category: Category) -> dict:
    return {
        'oid': category.oid,
        'title': category.title.as_generic_type(),
        'created_at': category.created_at,
    }


def convert_category_model_to_entity(category_model: Categories) -> Category:
    category_document = model_to_document(category_model)

    return Category(
        title=CategoryTitle(value=category_document["title"]),
        oid=category_document["oid"],
        created_at=category_document["created_at"],
    )
