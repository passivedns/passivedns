from typing import List
from flask import jsonify

from models.user import User
from models.user_request import UserRequest
from models.user_pending import UserPending


def user_request_list_view(user_request_list: List[UserRequest]):
    return jsonify({
        "msg": "requested user list retrieved",
        "user_request_list": [
            ur.json() for ur in user_request_list
        ]
    }), 200


def user_request_deleted_view(user_request: UserRequest):
    return jsonify({
        "msg": "user request removed",
        "user_request_list": [
            user_request.json()
        ]
    }), 200


def user_pending_list_view(user_pending_list: List[UserPending]):
    return jsonify({
        "msg": "requested user list retrieved",
        "user_pending_list": [
            up.safe_json() for up in user_pending_list
        ]
    }), 200


def user_list_view(user_list: List[User]):
    return jsonify({
        "msg": "user list retrieved",
        "user_list": [
            u.safe_json() for u in user_list
        ]
    }), 200


def user_deleted_view(user: User):
    return jsonify({
        "msg": f"user {user.username} deleted",
        "user": user.safe_json()
    }), 200


def user_pending_created_view(user_pending: UserPending):
    return jsonify({
        "msg": f"user with mail {user_pending.email} invited",
        "user_pending": user_pending.safe_json()
    }), 201
