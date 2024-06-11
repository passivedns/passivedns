from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from db.database import ObjectNotFound
from models.user import User
from models.user_pending import UserPending
from models.user_request import UserRequest
from models.channel import Channel
from models.user_channel import UserChannel
from models.api_integration import APIIntegration
from analytics.extern_api import ExternAPI, RequestException

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
    if User.exists(user_data.username):
        raise HTTPException(
            status_code=500,
            detail=f"user with username `{user_data.username}` already exists",
        )

    try:
        user_pending = UserPending.get(user_data.token)
    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=f"user pending not found: {str(o)}")

    created_user = User.new(user_data.username, user_data.password, user_pending.email)
    created_user.insert()
    user_pending.delete()

    try:
        default_channel = Channel.get(Channel.DEFAULT)
    except ObjectNotFound as o:
        raise HTTPException(
            status_code=404, detail=f"default channel not found: {str(o)}"
        )
    user_channel = UserChannel.new(
        created_user.username, default_channel.name, created_user.email
    )
    user_channel.verified = True
    user_channel.insert()

    return {
        "msg": f"user {created_user.username} created",
        "user": created_user.safe_json(),
    }


# require a token from the UsersPending table (sent by email)
@users_router.post("/register/check")
def token_check(token_data: CheckToken):
    token = token_data.token

    if UserPending.exists(token):
        return {"msg": "valid token"}
    else:
        raise HTTPException(status_code=400, detail="invalid token")


# require nothing
@users_router.post("/request")
def request_access(access_data: Access):
    email = access_data.email

    if User.exists_from_email(email):
        raise HTTPException(status_code=500, detail="email unavailable")

    if UserPending.exists_from_email(email):
        raise HTTPException(
            status_code=500, detail="an invitation has already been sent to this email"
        )

    if UserRequest.exists(email):
        raise HTTPException(
            status_code=500, detail="a request for this email has already been sent"
        )

    user_request = UserRequest.new(email)
    user_request.insert()

    return {
        "msg": f"request for access with mail {user_request.email} sent to admin",
        "user_request": user_request.json(),
    }


@users_router.put("/password", dependencies=[Depends(get_current_user)])
def change_password(
    password_data: ChangePassword, current_user: User = Depends(get_current_user)
):
    current_password = password_data.current_password
    new_password = password_data.new_password

    username = current_user.username
    user = User.get(username)
    if not user.verify_password(current_password):
        raise HTTPException(status_code=401, detail="invalid password")

    if new_password == current_password:
        raise HTTPException(status_code=400, detail="new password same as current")

    user.update_password(new_password)

    return {"msg": "password changed"}

@users_router.post("/apikey/{api_name}", dependencies=[Depends(get_current_user)])
def add_api_key(api_name, api_key: str, user: User = Depends(get_current_user)):

    #check api exists
    try:
        api = APIIntegration.get(api_name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Extern API not found")

    #check key is valid
    try :
        ExternAPI(api, api_key).testRequest()
    except RequestException as r:
        raise HTTPException(status_code=r.status_code, detail=f"Error : {r.message}")

    user.update_api_keys(api_name, api_key)

    return {"msg": f"Key for api {api_name} added to user {user.username}"}
