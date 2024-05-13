from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from channels.email import MailSendingError
from channels.send import send
from channels.telegram import TelegramSendingError
from channels.templates_list import INVITE_TEMPLATE
from apiv2.auth import check_admin_role
from db.database import ObjectNotFound
from models.channel import Channel
from models.user import User, UserRole
from models.user_pending import UserPending
from models.user_request import UserRequest
from models.user_channel import UserChannel

users_admin_router = APIRouter()

class DeleteRequest(BaseModel):
    email: str

class DeleteUser(BaseModel):
    username: str

class Invite(BaseModel):
    email: str

class VerifyUser(BaseModel):
    email: str

# get the list of all the requested access
# require admin JWT
@users_admin_router.get("/admin/request/list", dependencies =[Depends(check_admin_role)]) 
def request_list():
    user_request_list = UserRequest.list()
    return {
        "msg": "requested user list retrieved",
        "user_request_list": [
            ur.json() for ur in user_request_list
        ]
    }


# remove a user access
# require admin JWT
@users_admin_router.delete("/admin/request", dependencies =[Depends(check_admin_role)])
def request_remove(user_data: DeleteRequest):
    try:
        email = user_data.email

        user_request = UserRequest.get(email)
        user_request.delete()

        return {
            "msg": "user request removed",
            "user_request_list": [
                user_request.json()
            ]
        }

    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="object not found")


# get the list of all the requested access
# require admin JWT
@users_admin_router.get("/admin/invite/list", dependencies =[Depends(check_admin_role)])
def pending_list():
    user_invite_list = UserPending.list()
    return {
        "msg": "requested user list retrieved",
        "user_pending_list": [
            up.safe_json() for up in user_invite_list
        ]
    }


# the list of the users registered
# require admin JWT
@users_admin_router.get("/admin/users/list", dependencies =[Depends(check_admin_role)])
def get_user_list():
    user_list = User.list()
    return {
        "msg": "user list retrieved",
        "user_list": [
            u.safe_json() for u in user_list
        ]
    }


# remove a user
# require admin JWT
@users_admin_router.delete("/admin/users", dependencies =[Depends(check_admin_role)])
def remove_user(user_data: DeleteUser):
    username = user_data.username

    user = User.get(username)
    if user.role != UserRole.ADMIN.value:
        user.delete()

        user_channels = UserChannel.list_from_username(user.username)
        for user_ch in user_channels:
            user_ch.delete()

        return {
            "msg": f"user {user.username} deleted",
            "user": user.safe_json()
        }

    else:
        raise HTTPException(status_code=500, detail="cannot remove an admin user")


# require admin JWT
@users_admin_router.post("/admin/invite", dependencies =[Depends(check_admin_role)])
def invite(user_data: Invite):
    user_pending = None

    try:
        email = user_data.email

        # check if mail is already used
        if User.exists_from_email(email):
            raise HTTPException(status_code=500, detail=f"email already used by an existing user")

        if UserRequest.exists(email):
            raise HTTPException(status_code=500, detail=f"a request for this email already exists")

        if UserPending.exists_from_email(email):
            raise HTTPException(status_code=500, detail=f"a user with this email has already been invited")

        # create a new pending user in database
        user_pending = UserPending.new(email)
        user_pending.insert()

        # send a mail with the token
        default_channel = Channel.get(Channel.DEFAULT)
        template = INVITE_TEMPLATE
        template.set_format(token=user_pending.token)
        send(
            user_pending.email,
            default_channel,
            template
        )

        return {
            "msg": f"user with mail {user_pending.email} invited",
            "user_pending": user_pending.safe_json()
        }

    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=str(o))

    except (MailSendingError, TelegramSendingError):
        # in case the mail cannot be sent, abort the invitation and delete the pending user in database
        if user_pending is not None:
            user_pending.delete()

        raise HTTPException(status_code=500, detail=f"error sending the invitation")


@users_admin_router.post("/admin/verify", dependencies =[Depends(check_admin_role)])
def verify_requested_user(user_data: VerifyUser):
    user_pending = None
    try:
        email = user_data.email

        if User.exists_from_email(email):
            raise HTTPException(status_code=500, detail="a user with this email already exists")
        
        if not UserRequest.exists(email):
            raise HTTPException(status_code=404, detail="a request with this email not found")


        # switch user request to user pending
        user_request = UserRequest.get(email)
        user_request.delete()

        user_pending = UserPending.new(email)
        user_pending.insert()

        # send mail with token
        # send a mail with the token
        default_channel = Channel.get(Channel.DEFAULT)
        template = INVITE_TEMPLATE
        template.set_format(token=user_pending.token)
        send(
            user_pending.email,
            default_channel,
            template
        )
        return {
            "msg": f"user with mail {user_pending.email} invited",
            "user_pending": user_pending.safe_json()
        }

    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=str(o))

    except (MailSendingError, TelegramSendingError):
        # in case the mail cannot be sent, abort the invitation and delete the pending user in database
        if user_pending is not None:
            user_pending.delete()

        raise HTTPException(status_code=500, detail=f"error sending the invitation")
