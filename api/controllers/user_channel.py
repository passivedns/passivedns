from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from channels.email import MailSendingError
from channels.send import send
from channels.telegram import TelegramSendingError
from channels.templates_list import CHANNEL_VERIFY_TEMPLATE, TEST_TEMPLATE
from controllers.utils import check_scheduler_role, check_admin_user_role
from views.misc import error_view
from views.user_channel import *
from db.database import ObjectNotFound
from models.channel import Channel
from models.user_channel import UserChannel
from models.user import User
from utils import config, timezone

users_channel_blueprint = Blueprint("user_channels", __name__)


# get the list of channels setup by the user
@users_channel_blueprint.route("/user/channels", methods=['GET'])
@jwt_required()
@check_admin_user_role()
def users_channel_list():
    username = get_jwt_identity()

    out = []
    user_channels = UserChannel.list_from_username(username)
    for u_ch in user_channels:
        channel = Channel.get(u_ch.channel_name)
        out.append({
            'user_channel': u_ch,
            'channel': channel
        })

    return user_ch_list_view(out)


def user_channel_get(channel_name, username):
    try:
        user_channel = UserChannel.get(username, channel_name)
        return user_ch_get_view(user_channel)
    except ObjectNotFound:
        return error_view(404, "user channel not found")


def user_channel_post(channel_name, username):
    new_user_channel = None
    try:
        contact = request.args.get('contact')
        if contact is None or contact == '':
            return error_view(400, "invalid contact")

        channel = Channel.get(channel_name)
        user = User.get(username)

        if UserChannel.exists(user.username, channel.name):
            return error_view(500, "this channel is already linked")

        new_user_channel = UserChannel.new(user.username, channel.name, contact)
        new_user_channel.insert()

        template = CHANNEL_VERIFY_TEMPLATE
        template.set_format(token=new_user_channel.token, channel=channel.name)
        send(contact, channel, template)

        return user_ch_created_view(new_user_channel)

    except (MailSendingError, TelegramSendingError):
        if new_user_channel is not None:
            new_user_channel.delete()

        return error_view(500, "error sending token to this contact")


def user_channel_put(channel_name, username):
    try:
        token = request.args.get('token')
        if token is None or token == '':
            return error_view(400, 'missing token')

        user_channel = UserChannel.get(username, channel_name)
        if user_channel.verified:
            return error_view(500, 'this channel has already been verified')

        if token != user_channel.token:
            return error_view(500, 'invalid token')

        user_channel.update(verified=True)
        return user_ch_updated_view(user_channel)

    except ObjectNotFound:
        return error_view(404, "user channel not found")


def user_channel_delete(channel_name, username):
    try:
        if channel_name == Channel.DEFAULT:
            return error_view(500, "cannot unlink default channel")

        user_channel = UserChannel.get(username, channel_name)
        user_channel.delete()
        return user_ch_deleted_view(user_channel)
    except ObjectNotFound:
        return error_view(404, "user channel not found")


@users_channel_blueprint.route("/user/channels/<channel_name>", methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required()
@check_admin_user_role()
def channel_manage(channel_name):
    username = get_jwt_identity()
    if request.method == 'GET':
        return user_channel_get(channel_name, username)

    elif request.method == 'POST':
        return user_channel_post(channel_name, username)

    elif request.method == 'PUT':
        return user_channel_put(channel_name, username)

    elif request.method == 'DELETE':
        return user_channel_delete(channel_name, username)


@users_channel_blueprint.route("/user/channels/<channel_name>/test", methods=['GET'])
@jwt_required()
@check_admin_user_role()
def channel_test(channel_name):
    try:
        username = get_jwt_identity()
        if request.method == 'GET':
            user = User.get(username)
            channel = Channel.get(channel_name)
            user_channel = UserChannel.get(user.username, channel.name)

            template = TEST_TEMPLATE
            date = timezone.get_current_datetime(config.g.TIMEZONE)
            template.set_format(date=str(date))
            send(user_channel.contact, channel, template)

            return user_ch_test_view(user_channel)

    except ObjectNotFound:
        return error_view(404, "object not found")

    except (MailSendingError, TelegramSendingError):
        return error_view(500, "failed to send test")
