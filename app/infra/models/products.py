from decimal import Decimal
from typing import Any
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infra.models.base import BaseModel


class Products(BaseModel):
    __tablename__ = "products"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(nullable=False)
    image_oid: Mapped[UUID] = mapped_column(ForeignKey("product_images.oid"), nullable=True)
    category_oid: Mapped[UUID] = mapped_column(ForeignKey("categories.oid"), nullable=False)
    characteristics: Mapped[dict[str, Any]] = mapped_column(nullable=False)
