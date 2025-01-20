from typing import Any
from domain.entities.carts import Cart


def convert_cart_entity_to_document(cart: Cart) -> dict[str, Any]:
    return {
        'oid': cart.oid,
        'created_at': cart.created_at,
    }
