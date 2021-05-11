from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from controllers.utils import check_admin_role
from models.user import User
from views.misc import error_view
from views.scheduler import scheduler_created_view, scheduler_updated_view, scheduler_deleted_view

scheduler_admin_blueprint = Blueprint("scheduler_admin", __name__)


def get_password_json():
    body = request.json
    if body is None:
        return None

    password = body.get('password')
    if password is None or password == '':
        return None

    return password


def post(scheduler_name):
    if User.exists(scheduler_name):
        return error_view(500, "name unavailable")

    password = get_password_json()
    if password is None:
        return error_view(400, 'invalid parameter')

    admin_user = User.get(get_jwt_identity())
    new_scheduler = User.new(scheduler_name, password, admin_user.email, is_scheduler=True)
    new_scheduler.insert()

    return scheduler_created_view(new_scheduler)


def put(scheduler_name):
    if not User.exists(scheduler_name):
        return error_view(404, "scheduler not found")

    password = get_password_json()
    if password is None:
        return error_view(400, 'invalid parameter')

    scheduler = User.get(scheduler_name)
    scheduler.update_password(password)

    return scheduler_updated_view(scheduler)


@scheduler_admin_blueprint.route("/admin/scheduler/<scheduler_name>", methods=['POST', 'PUT'])
@jwt_required()
@check_admin_role()
def manage_scheduler(scheduler_name):
    if request.method == 'POST':
        return post(scheduler_name)

    elif request.method == 'PUT':
        return put(scheduler_name)
