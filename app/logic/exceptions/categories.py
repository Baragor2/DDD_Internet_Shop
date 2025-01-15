from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class CategoryWithThatTitleAlreadyExistsException(LogicException):
    title: str

    @property
    def message(self):
        return f'Category with such a title "{self.title}" already exists.'

