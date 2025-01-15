from sqlalchemy.orm import Mapped, mapped_column

from infra.models.base import BaseModel


class Categories(BaseModel):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(nullable=False, unique=True)
