from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infra.models.base import BaseModel


class Orders(BaseModel):
    __tablename__ = "orders"

    user_oid: Mapped[UUID] = mapped_column(ForeignKey("users.oid"), nullable=False)
    price: Mapped[Decimal] = mapped_column(nullable=False)
