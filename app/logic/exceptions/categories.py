from dataclasses import dataclass
from uuid import UUID

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class CategoryWithThatTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'Category with such a title "{self.title}" already exists.'


@dataclass(eq=False)
class CategoryWithThatTitleNotExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'Category with such a title "{self.title}" not exists.'


@dataclass(eq=False)
class CategoryWithThatOidNotExistsException(LogicException):
    oid: UUID

    @property
    def message(self):
        return f'Category with such oid "{self.oid}" not exists.'
