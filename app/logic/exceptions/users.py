from dataclasses import dataclass

from logic.exceptions.base import LogicException


@dataclass(eq=False)
class UserWithThatEmailAlreadyExistsException(LogicException):
    email: str

    @property
    def message(self):
        return f'User with such an email "{self.email}" already exists.'


@dataclass(eq=False)
class IncorrectEmailOrPasswordException(LogicException):
    @property
    def message(self):
        return f"Incorrect email or password exception."
