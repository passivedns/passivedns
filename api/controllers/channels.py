from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from controllers.utils import check_admin_user_role
from models.channel import Channel
from models.user_channel import UserChannel
from db.database import ObjectNotFound
from views.channels import *
from views.misc import error_view

channels_blueprint = Blueprint("channels", __name__)


# get the list of all available channels
@channels_blueprint.route("/channels", methods=['GET'])
@jwt_required()
@check_admin_user_role()
def channels_list():
    ch_list = Channel.list()

    username = get_jwt_identity()
    user_ch_list = UserChannel.list_from_username(username)

    out = []
    for ch in ch_list:
        found = False
        for u_ch in user_ch_list:
            if u_ch.channel_name == ch.name:
                found = True
                break
        if not found:
            out.append(ch)

    return ch_list_view(out)


@channels_blueprint.route("/channels/<channel_name>", methods=['GET'])
@jwt_required()
@check_admin_user_role()
def channel_get(channel_name):
    try:
        ch = Channel.get(channel_name)
        return ch_get_view(ch)
    except ObjectNotFound:
        return error_view(500, "channel not found")
