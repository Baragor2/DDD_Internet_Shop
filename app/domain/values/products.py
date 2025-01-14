from dataclasses import dataclass
from decimal import Decimal

from domain.exceptions.base import EmptyTextException
from domain.values.base import BaseValueObject
from domain.exceptions.products import DescriptionTooLongException, NegativePriceException, ProductTitleTooLongException


@dataclass(frozen=True)
class ProductTitle(BaseValueObject[str]):
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 255:
            raise ProductTitleTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Description(BaseValueObject[str]):
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 5000:
            raise DescriptionTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Price(BaseValueObject[Decimal]):
    def validate(self) -> None:
        if self.value < 0:
            raise NegativePriceException()
        
    def as_generic_type(self) -> Decimal:
        return Decimal(self.value)
    

@dataclass(frozen=True)
class CharacteristicTitle(BaseValueObject[str]):
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 255:
            raise ProductTitleTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)
