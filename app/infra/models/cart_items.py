from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infra.models.base import BaseModel


class CartItems(BaseModel):
    __tablename__ = "cart_items"

    cart_oid: Mapped[UUID] = mapped_column(ForeignKey("carts.oid"), nullable=False)
    order_oid: Mapped[UUID] = mapped_column(ForeignKey("orders.oid"), nullable=True)
    product_oid: Mapped[UUID] = mapped_column(ForeignKey("products.oid"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
