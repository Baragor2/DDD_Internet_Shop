from dataclasses import dataclass
from decimal import Decimal

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ProductTitleTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Too long product title "{self.text[:255]}..."'


@dataclass(eq=False)
class DescriptionTooLongException(ApplicationException):
    text: str

    @property
    def message(self):
        return f'Too long text "{self.text[:5000]}..."'


@dataclass(eq=False)
class NegativePriceException(ApplicationException):
    price: Decimal

    @property
    def message(self):
        return f'Price value can`t be nagative: {self.price}'
    
    