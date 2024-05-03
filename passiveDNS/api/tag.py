from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from api.utils import check_scheduler_role, check_admin_user_role
from views.misc import error_view
from views.tag import *
from models.tag import Tag
from models.tag_dn_ip import TagDnIP

tag_blueprint = Blueprint("tag", __name__)


def post(tag_name):
    if Tag.exists(tag_name):
        return error_view(500, "tag already exists")

    new_tag = Tag.new(tag_name)
    new_tag.insert()

    return tag_created_view(new_tag)


def delete(tag_name):
    if not Tag.exists(tag_name):
        return error_view(404, "tag not found")

    tag = Tag.get(tag_name)
    tag.delete()

    tag_links = TagDnIP.list_from_tag(tag.name)
    for t in tag_links:
        t.delete()

    return tag_deleted_view(tag)


@tag_blueprint.route("/tag/<tag_name>", methods=['POST', 'DELETE'])
@jwt_required()
@check_admin_user_role()
def manage_tag(tag_name):
    if request.method == 'POST':
        return post(tag_name)
    elif request.method == 'DELETE':
        return delete(tag_name)


@tag_blueprint.route("/tag", methods=['GET'])
@jwt_required()
@check_admin_user_role()
def manage_tag_list():
    return tag_list_view(Tag.list())
