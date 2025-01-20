from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class WrongRoleException(ApplicationException):
    role: str

    @property
    def message(self):
        return f"Wrong role: {self.role}."
    

@dataclass(eq=False)
class UserNameTooLongException(ApplicationException):
    username: str

    @property
    def message(self):
        return f'Too long username "{self.text[:255]}..."'
    

@dataclass(eq=False)
class WrongEmailException(ApplicationException):
    email: str

    @property
    def message(self):
        return f'Wrong email "{self.email}."'
