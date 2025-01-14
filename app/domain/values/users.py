from dataclasses import dataclass

from domain.exceptions.base import EmptyTextException
from domain.exceptions.users import UserNameTooLongException, WrongRoleException
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