from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infra.models.base import BaseModel


class Carts(BaseModel):
    __tablename__ = "carts"

    user_oid: Mapped[UUID] = mapped_column(ForeignKey("users.oid"), nullable=False, unique=True)