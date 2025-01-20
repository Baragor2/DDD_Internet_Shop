from typing import Any
from domain.entities.users import User


def convert_user_entity_to_document(user: User) -> dict[str, Any]:
    return {
        'oid': user.oid,
        'created_at': user.created_at,
        'username': user.username.as_generic_type(),
        'email': user.email.as_generic_type(),
        'password_hash': user.password_hash,
        'role': user.role.role.as_generic_type(),
        'is_active': user.is_active,
        'cart_oid': user.cart_oid,
    }
