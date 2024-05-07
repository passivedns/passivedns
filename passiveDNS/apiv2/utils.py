from functools import wraps

from fastapi import HTTPException
from apiv2.auth import get_current_user

from models.user import User, UserRole


def check_admin_user_role():
    """
    Check if the JWT belongs to a User or an Admin
    :return: error view if condition not reached
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_current_user()
            current_username = current_user.username
            user = User.get(current_username)
            if user.role != UserRole.USER.value and user.role != UserRole.ADMIN.value:
                raise HTTPException(status_code=403, detail="not enough permission")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_scheduler_role():
    """
    Check if the JWT belongs to a Scheduler
    :return: error view if condition not reached
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_current_user()
            current_username = current_user.username
            user = User.get(current_username)
            if user.role != UserRole.SCHEDULER.value:
                raise HTTPException(status_code=403, detail="not enough permission")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def check_admin_role():
    """
    Check if the JWT belongs to an Admin
    :return: error view if condition not reached
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = get_current_user()
            current_username = current_user.username
            user = User.get(current_username)
            if user.role != UserRole.ADMIN.value:
                raise HTTPException(status_code=403, detail="not enough permission")

            return func(*args, **kwargs)

        return wrapper

    return decorator
