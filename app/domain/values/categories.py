from dataclasses import dataclass

from domain.exceptions.base import EmptyTextException
from domain.exceptions.categories import CategoryTitleTooLongException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class CategoryTitle(BaseValueObject[str]):
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 500:
            raise CategoryTitleTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)
