from typing import Any
from domain.values.users import Email, UserName
from infra.repositories.converters import model_to_document
from domain.entities.users import User


def convert_user_entity_to_document(user: User) -> dict[str, Any]:
    return {
        "oid": user.oid,
        "created_at": user.created_at,
        "username": user.username.as_generic_type(),
        "email": user.email.as_generic_type(),
        "password_hash": user.password_hash,
        "role": user.role.role.as_generic_type(),
        "is_active": user.is_active,
        "cart_oid": user.cart_oid,
    }


def convert_user_model_to_entity(user_model: User) -> User:
    user_document = model_to_document(user_model)

    return User(
        oid=user_document["oid"],
        username=UserName(value=user_document["username"]),
        created_at=user_document["created_at"],
        email=Email(user_document["email"]),
        password_hash=user_document["password_hash"],
        role=user_document["role"],
        is_active=user_document["is_active"],
        cart_oid=user_document["cart_oid"],
    )
