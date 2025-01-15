from domain.entities.categories import Category


def convert_category_entity_to_document(category: Category) -> dict:
    return {
        'oid': category.oid,
        'title': category.title.as_generic_type(),
        'created_at': category.created_at,
    }
