from fastapi import APIRouter
from pydantic import BaseModel

from channels.email import MailSendingError
from channels.send import send
from channels.telegram import TelegramSendingError
from channels.templates_list import INVITE_TEMPLATE
from apiv2.utils import check_admin_user_role
from db.database import ObjectNotFound
from models.channel import Channel
from models.user import User, UserRole
from models.user_pending import UserPending
from models.user_request import UserRequest
from models.user_channel import UserChannel
from views.misc import error_view
from views.users_admin import *

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
@users_admin_router.get("/admin/request/list")
@check_admin_user_role()
def request_list():
    user_request_list = UserRequest.list()
    return user_request_list_view(user_request_list)


# remove a user access
# require admin JWT
@users_admin_router.delete("/admin/request")
@check_admin_user_role()
def request_remove(user_data: DeleteRequest):
    try:
        email = user_data.email

        user_request = UserRequest.get(email)
        user_request.delete()

        return user_request_deleted_view(user_request)

    except ObjectNotFound:
        return error_view(404, "object not found")


# get the list of all the requested access
# require admin JWT
@users_admin_router.get("/admin/invite/list")
@check_admin_user_role()
def pending_list():
    user_invite_list = UserPending.list()
    return user_pending_list_view(user_invite_list)


# the list of the users registered
# require admin JWT
@users_admin_router.get("/admin/users/list")
@check_admin_user_role()
def get_user_list():
    user_list = User.list()
    return user_list_view(user_list)


# remove a user
# require admin JWT
@users_admin_router.delete("/admin/users")
@check_admin_user_role()
def remove_user(user_data: DeleteUser):
    username = user_data.username

    user = User.get(username)
    if user.role != UserRole.ADMIN.value:
        user.delete()

        user_channels = UserChannel.list_from_username(user.username)
        for user_ch in user_channels:
            user_ch.delete()

        return user_deleted_view(user)

    else:
        return error_view(500, "cannot remove an admin user")


# require admin JWT
@users_admin_router.post("/admin/invite")
@check_admin_user_role()
def invite(user_data: Invite):
    user_pending = None

    try:
        email = user_data.email
        if email is None:
            return error_view(400, "invalid email value")

        # check if mail is already used
        if User.exists_from_email(email):
            return error_view(500, f"email already used by an existing user")

        if UserRequest.exists(email):
            return error_view(500, f"a request for this email already exists")

        if UserPending.exists_from_email(email):
            return error_view(500, f"a user with this email has already been invited")

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

        return user_pending_created_view(user_pending)

    except ObjectNotFound as o:
        return error_view(404, str(o))

    except (MailSendingError, TelegramSendingError):
        # in case the mail cannot be sent, abort the invitation and delete the pending user in database
        if user_pending is not None:
            user_pending.delete()

        return error_view(500, f"error sending the invitation")


@users_admin_router.post("/admin/verify")
@check_admin_user_role()
def verify_requested_user(user_data: VerifyUser):
    user_pending = None
    try:
        email = user_data.email

        if not UserRequest.exists(email):
            return error_view(404, "a request with this email not found")

        if User.exists_from_email(email):
            return error_view(500, "a user with this email already exists")

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
        return user_pending_created_view(user_pending)

    except ObjectNotFound as o:
        return error_view(404, str(o))

    except (MailSendingError, TelegramSendingError):
        # in case the mail cannot be sent, abort the invitation and delete the pending user in database
        if user_pending is not None:
            user_pending.delete()

        return error_view(500, f"error sending the invitation")
