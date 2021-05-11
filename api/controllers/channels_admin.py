from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from controllers.utils import check_admin_role
from views.channels_admin import *
from models.channel import Channel, ChannelTypeError
from models.user_channel import UserChannel
from views.misc import error_view

channels_admin_blueprint = Blueprint("channels_admin", __name__)


# get channel list - admin view
@channels_admin_blueprint.route("/admin/channels", methods=['GET'])
@jwt_required()
@check_admin_role()
def channels_admin_list():
    ch_list = Channel.list()
    return ch_admin_list_view(ch_list)


def ch_post(name):
    try:
        ch_type = request.args.get('type')
        if ch_type is None or ch_type == '':
            return error_view(400, "missing parameter")

        infos = request.json
        if infos is None or infos == '':
            return error_view(400, "missing json")

        if Channel.exists(name):
            return error_view(500, "a channel with this name already exists")

        new_ch = Channel.new(name, ch_type, infos)
        new_ch.insert()

        return ch_admin_post_view(new_ch)

    except KeyError:
        return error_view(500, "error parsing json input")

    except ChannelTypeError:
        return error_view(400, "invalid channel type")


def ch_get(name):
    if not Channel.exists(name):
        return error_view(404, f"channel {name} not found")
    ch = Channel.get(name)
    return ch_admin_get_view(ch)


def ch_put(name):
    infos = request.json
    if infos is None or infos == '':
        return error_view(400, "missing parameter")

    if not Channel.exists(name):
        return error_view(404, f"channel {name} not found")

    ch = Channel.get(name)
    ch.update(infos)

    return ch_admin_put_view(ch)


def ch_delete(name):
    if name == Channel.DEFAULT:
        return error_view(403, f"cannot modify default channel")

    if not Channel.exists(name):
        return error_view(404, f"channel {name} not found")

    ch = Channel.get(name)
    user_channel_list = UserChannel.list_from_channel(ch.name)
    for user_ch in user_channel_list:
        user_ch.delete()

    ch.delete()

    return ch_admin_delete_view(ch)


@channels_admin_blueprint.route(
    "/admin/channels/<name>", methods=['POST', 'GET', 'PUT', 'DELETE'])
@jwt_required()
@check_admin_role()
def channel_admin(name):
    if request.method == 'POST':
        return ch_post(name)

    elif request.method == 'GET':
        return ch_get(name)

    elif request.method == 'PUT':
        return ch_put(name)

    elif request.method == 'DELETE':
        return ch_delete(name)
