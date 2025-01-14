from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.types import JSON
from typing import Any


class Base(DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON
    }


class BaseModel(Base):
    __abstract__ = True

    oid: Mapped[UUID] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

