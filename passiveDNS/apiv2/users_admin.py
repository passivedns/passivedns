from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from passiveDNS.utils.channels.email import MailSendingError
from passiveDNS.utils.channels.send import send
from passiveDNS.utils.channels.telegram import TelegramSendingError
from passiveDNS.utils.channels.templates_list import INVITE_TEMPLATE
from passiveDNS.db.database import ObjectNotFound
from passiveDNS.models.channel import Channel
from passiveDNS.models.user import User, UserRole
from passiveDNS.models.user_pending import UserPending
from passiveDNS.models.user_request import UserRequest
from passiveDNS.models.user_channel import UserChannel

users_admin_router = APIRouter()


class Invite(BaseModel):
    email: str


class VerifyUser(BaseModel):
    email: str


# get the list of all the requested access
# require admin JWT
@users_admin_router.get("/admin/request/list")
async def request_list():
    user_request_list = UserRequest.list()
    return {
        "msg": "requested user list retrieved",
        "user_request_list": [ur.json() for ur in user_request_list],
    }


# remove a user access
# require admin JWT
@users_admin_router.delete("/admin/request/{email}")
async def request_remove(email: str):
    try:
        user_request = UserRequest.get(email)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="object not found")

    user_request.delete()

    return {"msg": "user request removed", "user_request": [user_request.json()]}


# get the list of all the requested access
# require admin JWT
@users_admin_router.get("/admin/invite/list")
async def pending_list():
    user_invite_list = UserPending.list()
    return {
        "msg": "requested user list retrieved",
        "user_pending_list": [up.safe_json() for up in user_invite_list],
    }


# the list of the users registered
# require admin JWT
@users_admin_router.get("/admin/users/list")
async def get_user_list():
    user_list = User.list()
    return {
        "msg": "user list retrieved",
        "user_list": [u.safe_json() for u in user_list],
    }


# remove a user
# require admin JWT
@users_admin_router.delete("/admin/users/{username}")
async def remove_user(username):
    try:
        user = User.get(username)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="user not found")

    if user.role != UserRole.ADMIN.value:
        user.delete()

        user_channels = UserChannel.list_from_username(user.username)
        for user_ch in user_channels:
            user_ch.delete()

        return {"msg": f"user {user.username} deleted", "user": user.safe_json()}

    else:
        raise HTTPException(status_code=500, detail="cannot remove an admin user")


# require admin JWT
@users_admin_router.post("/admin/invite")
async def invite(user_data: Invite):
    user_pending = None

    email = user_data.email

    # check if mail is already used
    if User.exists_from_email(email):
        raise HTTPException(
            status_code=500, detail="email already used by an existing user"
        )

    if UserRequest.exists(email):
        raise HTTPException(
            status_code=500, detail="a request for this email already exists"
        )

    if UserPending.exists_from_email(email):
        raise HTTPException(
            status_code=500, detail="a user with this email has already been invited"
        )

    # create a new pending user in database
    user_pending = UserPending.new(email)
    user_pending.insert()

    # send a mail with the token
    try:
        default_channel = Channel.get(Channel.DEFAULT)
    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=str(o))
    template = INVITE_TEMPLATE
    template.set_format(token=user_pending.token)

    try:
        send(user_pending.email, default_channel, template)
    except (MailSendingError, TelegramSendingError):
        # in case the mail cannot be sent, abort the invitation and delete the pending user in database
        if user_pending is not None:
            user_pending.delete()

        raise HTTPException(status_code=500, detail="error sending the invitation")

    return {
        "msg": f"user with mail {user_pending.email} invited",
        "user_pending": user_pending.safe_json(),
    }


@users_admin_router.post("/admin/verify")
async def verify_requested_user(user_data: VerifyUser):
    user_pending = None

    email = user_data.email

    if User.exists_from_email(email):
        raise HTTPException(
            status_code=500, detail="a user with this email already exists"
        )

    if not UserRequest.exists(email):
        raise HTTPException(
            status_code=404, detail="a request with this email not found"
        )

    # switch user request to user pending
    try:
        user_request = UserRequest.get(email)
    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=f"user not found: {str(o)}")
    user_request.delete()

    user_pending = UserPending.new(email)
    user_pending.insert()

    # send mail with token
    # send a mail with the token
    try:
        default_channel = Channel.get(Channel.DEFAULT)
    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=f"channel not found: {str(o)}")
    template = INVITE_TEMPLATE
    template.set_format(token=user_pending.token)
    try:
        send(user_pending.email, default_channel, template)
    except (MailSendingError, TelegramSendingError):
        # in case the mail cannot be sent, abort the invitation and delete the pending user in database
        if user_pending is not None:
            user_pending.delete()

        raise HTTPException(status_code=500, detail="error sending the invitation")

    return {
        "msg": f"user with mail {user_pending.email} invited",
        "user_pending": user_pending.safe_json(),
    }
