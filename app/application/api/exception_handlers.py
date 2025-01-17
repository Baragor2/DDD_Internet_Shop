from fastapi import HTTPException, status
from functools import wraps
from typing import Callable, TypeVar, Awaitable

from domain.exceptions.base import ApplicationException

T = TypeVar("T")


def handle_application_exceptions(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        try:
            return await func(*args, **kwargs)
        except ApplicationException as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={'error': exception.message},
            )
    return wrapper
