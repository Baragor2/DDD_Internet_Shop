from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from infra.models.base import BaseModel

class ProductImages(BaseModel):
    __tablename__ = 'product_images'

    product_id: Mapped[UUID] = mapped_column(nullable=False)
    image: Mapped[bytes] = mapped_column(nullable=False)
