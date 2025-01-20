from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from infra.models.base import BaseModel


class Carts(BaseModel):
    __tablename__ = "carts"
