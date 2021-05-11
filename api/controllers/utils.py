from functools import wraps

from flask_jwt_extended import get_jwt_identity

from views.misc import error_view
from models.user import User, UserRole


def check_admin_user_role():
    """
    Check if the JWT belongs to a User or an Admin
    :return: error view if condition not reached
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_username = get_jwt_identity()
            user = User.get(current_username)
            if user.role != UserRole.USER.value and user.role != UserRole.ADMIN.value:
                return error_view(403, "not enough permission")

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
            current_username = get_jwt_identity()
            user = User.get(current_username)
            if user.role != UserRole.SCHEDULER.value:
                return error_view(403, "not enough permission")

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
            current_username = get_jwt_identity()
            user = User.get(current_username)
            if user.role != UserRole.ADMIN.value:
                return error_view(403, "not enough permission")

            return func(*args, **kwargs)

        return wrapper

    return decorator
