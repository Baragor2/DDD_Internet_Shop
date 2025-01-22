from dataclasses import dataclass

from pydantic import EmailStr
from email_validator import validate_email

from domain.exceptions.base import EmptyTextException
from domain.exceptions.users import (
    UserNameTooLongException,
    WrongEmailException,
    WrongRoleException,
)
from domain.values.base import BaseValueObject


@dataclass(frozen=True)
class AdminRole(BaseValueObject[str]):
    def validate(self):
        if self.value != "Admin":
            raise WrongRoleException(self.value)

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class UserRole(BaseValueObject[str]):
    def validate(self):
        if self.value != "User":
            raise WrongRoleException(self.value)

    def as_generic_type(self):
        return str(self.value)


@dataclass(frozen=True)
class UserName(BaseValueObject[str]):
    def validate(self):
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 255:
            raise UserNameTooLongException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Email(BaseValueObject[str]):
    def validate(self):
        try:
            validate_email(self.value)
        except:
            raise WrongEmailException(self.value)

    def as_generic_type(self) -> str:
        return str(self.value)
