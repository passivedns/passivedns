from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from db.database import ObjectNotFound
from models.user import User
from models.user_pending import UserPending
from models.user_request import UserRequest
from models.channel import Channel
from models.user_channel import UserChannel
from views.misc import error_view, valid_view
from views.users import *

users_blueprint = Blueprint("users", __name__)


# require a token from the UsersPending table (sent by email)
@users_blueprint.route("/register", methods=['POST'])
def register():
    try:
        body = request.json
        if body is None:
            return error_view(400, "invalid JSON in body")

        username = body.get('username')
        password = body.get('password')
        token = request.args.get('token')

        if username is None or password is None or token is None:
            return error_view(400, "invalid parameters")

        if token == '' or username == '' or password == '':
            return error_view(400, "missing parameters")

        if User.exists(username):
            return error_view(500, f"user with username `{username}` already exists")

        user_pending = UserPending.get(token)
        created_user = User.new(username, password, user_pending.email)
        created_user.insert()
        user_pending.delete()

        default_channel = Channel.get(Channel.DEFAULT)
        user_channel = UserChannel.new(
            created_user.username,
            default_channel.name,
            created_user.email
        )
        user_channel.verified = True
        user_channel.insert()

        return user_created_view(created_user)

    except ObjectNotFound as o:
        return error_view(404, str(o))


# require a token from the UsersPending table (sent by email)
@users_blueprint.route("/register/check", methods=['POST'])
def token_check():
    token = request.args.get('token')
    if token is None or token == "":
        return error_view(400, "missing token")

    if UserPending.exists(token):
        return valid_view("valid token")
    else:
        return error_view(400, "invalid token")


# require nothing
@users_blueprint.route("/request", methods=['POST'])
def request_access():
    body = request.json
    if body is None:
        return error_view(400, "invalid JSON in body")

    email = body.get('email')
    if email is None:
        return error_view(400, "invalid email value")

    if User.exists_from_email(email):
        return error_view(500, "email unavailable")

    if UserPending.exists_from_email(email):
        return error_view(500, "an invitation has already been sent to this email")

    if UserRequest.exists(email):
        return error_view(500, "a request for this email has already been sent")

    user_request = UserRequest.new(email)
    user_request.insert()

    return user_request_created_view(user_request)


@users_blueprint.route("/password", methods=['PUT'])
@jwt_required()
def change_password():
    if request.method == 'PUT':
        body = request.json
        if body is None:
            return error_view(400, "invalid JSON in body")

        current_password = body.get('current_password')
        new_password = body.get('new_password')
        params = [current_password, new_password]
        for p in params:
            if p is None or p == '':
                return error_view(400, "invalid parameter")

        username = get_jwt_identity()
        user = User.get(username)
        if not user.verify_password(current_password):
            return error_view(401, "invalid password")

        if new_password == current_password:
            return error_view(400, "new password same as current")

        user.update_password(new_password)

        return valid_view("password changed")
