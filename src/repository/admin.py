from functools import wraps
from typing import Callable
from src.database.models import Role, User


# def check_permission(func: Callable):
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         if kwargs.user.role == Role.admin or kwargs.user.role == Role.moder:
#             return await func(*args, **kwargs)

#     return wrapper

def check_permission(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = None
        for arg in args:
            if isinstance(arg, User):
                user = arg
                break
        else:
            for _, arg in kwargs.items():
                if isinstance(arg, User):
                    user = arg
                    break
            else:
                return None
        # print(f"[PE] user is {user.role}/{id(user)}")
        if user.role == Role.admin or user.role == Role.moder:
            return await func(*args, **kwargs)

    return wrapper
