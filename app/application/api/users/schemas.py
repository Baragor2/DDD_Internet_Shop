from typing import Any
from uuid import UUID
from pydantic import BaseModel, EmailStr

from domain.entities.users import User


class CreateUserRequestSchema(BaseModel):
    username: str
    email: str
    password: str


class CreateUserResponseSchema(BaseModel):
    oid: UUID
    username: str
    email: str
    role: str
    is_active: bool
    cart_oid: UUID

    @classmethod
    def from_entity(cls, user: User) -> "CreateUserResponseSchema":
        return cls(
            oid=user.oid,
            username=user.username.as_generic_type(),
            email=user.email.as_generic_type(),
            role=user.role.role.as_generic_type(),
            is_active=user.is_active,
            cart_oid=user.cart_oid,
        )


class LoginUserRequestSchema(BaseModel):
    email: str
    password: str
