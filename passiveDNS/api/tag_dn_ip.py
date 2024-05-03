from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from api.utils import check_scheduler_role, check_admin_user_role
from views.misc import error_view
from models.tag_dn_ip import TagDnIP
from models.tag import Tag
from models.domain_name import DOMAIN_NAME_COLLECTION, DomainName
from models.ip_address import IP_ADDRESS_COLLECTION, IPAddress
from views.tag_dn_ip import *

tag_dn_ip_blueprint = Blueprint("tag_dn_ip", __name__)


def post(tag_name, object_key, object_type):
    if TagDnIP.exists(tag_name, object_key, object_type):
        return error_view(500, "tag link already exists")

    if not Tag.exists(tag_name):
        return error_view(404, "source tag not found")

    if object_type == DOMAIN_NAME_COLLECTION:
        object_exists = DomainName.exists(object_key)
    elif object_type == IP_ADDRESS_COLLECTION:
        object_exists = IPAddress.exists(object_key)
    else:
        return error_view(400, "invalid object type")

    if not object_exists:
        return error_view(404, "target object not found")

    new_tag_link = TagDnIP.new(tag_name, object_key, object_type)
    new_tag_link.insert()

    return tag_link_created_view(new_tag_link)


def delete(tag, object_key, object_type):
    if not TagDnIP.exists(tag, object_key, object_type):
        return error_view(404, "tag link not found")

    tag_link = TagDnIP.get(tag, object_key, object_type)
    tag_link.delete()

    return tag_link_deleted_view(tag_link)


@tag_dn_ip_blueprint.route("/tag_dn_ip", methods=['POST', 'DELETE'])
@jwt_required()
@check_admin_user_role()
def manage_tag_dn_ip():
    tag = request.args.get('tag')
    object_key = request.args.get('object')
    object_type = request.args.get('type')

    params = [tag, object_key, object_type]
    for p in params:
        if p is None or p == '':
            return error_view(400, "invalid parameter")

    if request.method == 'POST':
        return post(tag, object_key, object_type)

    elif request.method == 'DELETE':
        return delete(tag, object_key, object_type)


@tag_dn_ip_blueprint.route("/tag_dn_ip/list/from", methods=['GET'])
@jwt_required()
@check_admin_user_role()
def manage_tag_dn_ip_list():
    object_key = request.args.get('object')
    object_type = request.args.get('type')

    params = [object_key, object_type]
    for p in params:
        if p is None or p == '':
            return error_view(400, "invalid parameter")

    tag_linked_list = TagDnIP.list_tags_from_object(object_key, object_type)
    return tag_link_list_view(tag_linked_list)
