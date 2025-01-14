from dataclasses import dataclass
from uuid import UUID

from pydantic import EmailStr

from domain.entities.base import BaseEntity
from domain.values.users import AdminRole, UserName, UserRole


@dataclass(eq=False)
class Role:
    role: AdminRole | UserRole
    

@dataclass(eq=False)
class User(BaseEntity):
    username: UserName
    email: EmailStr
    password_hash: bytes
    role: Role
    is_active: bool
    cart_oid: UUID

    @classmethod
    def create_user(
        cls,
        username: UserName,
        email: EmailStr,
        password_hash: bytes,
        role: Role,
        is_active: bool,
        cart_oid: UUID,
    ) -> 'User':
        new_user = cls(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            is_active=is_active,
            cart_oid=cart_oid,
        )

        return new_user