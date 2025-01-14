from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class WrongQuantityException(ApplicationException):
    quantity: int

    @property
    def message(self):
        return f'Wrong quantity: {self.quantity}'
    
 