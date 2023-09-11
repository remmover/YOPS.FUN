from functools import wraps
from typing import Callable
from src.database.models import Role


def check_permission(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if kwargs.user.role == Role.admin or kwargs.user.role == Role.moder:
            return await func(*args, **kwargs)

    return wrapper
