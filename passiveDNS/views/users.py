from models.user import User
from models.user_request import UserRequest


def user_created_view(user: User):
    return {
        "msg": f"user {user.username} created",
        "user": user.safe_json()
    }, 201


def user_request_created_view(user_request: UserRequest):
    return {
        "msg": f"request for access with mail {user_request.email} sent to admin",
        "user_request": user_request.json()
    }, 201

