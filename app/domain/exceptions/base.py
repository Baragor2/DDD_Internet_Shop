from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    @property
    def message(self):
        return "Application error occured"


@dataclass(eq=False)
class EmptyTextException(ApplicationException):
    @property
    def message(self):
        return "Text can`t be empty"
