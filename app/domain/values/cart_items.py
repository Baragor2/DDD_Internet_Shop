from dataclasses import dataclass

from domain.exceptions.cart_items import WrongQuantityException
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Quantity(BaseValueObject[int]):
    def validate(self) -> None:
        if self.value < 1:
            raise WrongQuantityException()
        
    def as_generic_type(self) -> int:
        return int(self.value)
 