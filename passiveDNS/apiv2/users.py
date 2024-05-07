from fastapi import APIRouter, Depends
from pydantic import BaseModel

from db.database import ObjectNotFound
from models.user import User
from models.user_pending import UserPending
from models.user_request import UserRequest
from models.channel import Channel
from models.user_channel import UserChannel
from views.misc import error_view, valid_view
from views.users import *

from apiv2.auth import get_current_user

users_router = APIRouter()

class UserRegistration(BaseModel):
    username: str
    password: str
    token: str

class CheckToken(BaseModel):
    token: str

class Access(BaseModel):
    email: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str

# require a token from the UsersPending table (sent by email)
@users_router.post("/register")
def register(user_data: UserRegistration):
    try:
        if User.exists(user_data.username):
            return error_view(500, f"user with username `{user_data.username}` already exists")

        user_pending = UserPending.get(user_data.token)
        created_user = User.new(user_data.username, user_data.password, user_pending.email)
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
@users_router.post("/register/check")
def token_check(token_data: CheckToken):
    token = token_data.token

    if UserPending.exists(token):
        return valid_view("valid token")
    else:
        return error_view(400, "invalid token")


# require nothing
@users_router.post("/request")
def request_access(access_data: Access):

    email = access_data.email

    if User.exists_from_email(email):
        return error_view(500, "email unavailable")

    if UserPending.exists_from_email(email):
        return error_view(500, "an invitation has already been sent to this email")

    if UserRequest.exists(email):
        return error_view(500, "a request for this email has already been sent")

    user_request = UserRequest.new(email)
    user_request.insert()

    return user_request_created_view(user_request)


@users_router.put("/password",dependencies=[Depends(get_current_user)])
def change_password(password_data: ChangePassword, current_user: User= Depends(get_current_user)):

    current_password = password_data.current_password
    new_password = password_data.new_password
    params = [current_password, new_password]
    for p in params:
        if p is None or p == '':
            return error_view(400, "invalid parameter")

    username = current_user.username
    user = User.get(username)
    if not user.verify_password(current_password):
        return error_view(401, "invalid password")

    if new_password == current_password:
        return error_view(400, "new password same as current")

    user.update_password(new_password)

    return valid_view("password changed")
