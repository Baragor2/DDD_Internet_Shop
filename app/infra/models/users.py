from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infra.models.base import BaseModel


class Users(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    cart_oid: Mapped[UUID] = mapped_column(
        ForeignKey("carts.oid"), nullable=False, unique=True
    )
