from functools import wraps
from typing import Generic, TypeVar, Callable

from pydantic import BaseModel


DataT = TypeVar("DataT")


class StandardResponse(BaseModel, Generic[DataT]):
    """Schema for standard response"""

    success: bool = True
    message: str = "Success"
    data: DataT | None = None


def wrap_response(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        return StandardResponse(success=True, message="Success", data=result)

    return wrapper
