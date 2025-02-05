from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class CategoryTitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Too long category title "{self.text[:500]}..."'
