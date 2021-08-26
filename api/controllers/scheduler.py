from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from channels.send import alert_all
from controllers.domain_name import put
from controllers.utils import check_scheduler_role
from views.domain_name import dn_modified_view
from views.misc import valid_view, error_view
from views.scheduler import dn_full_list_view
from models.domain_name import DomainName

scheduler_blueprint = Blueprint("scheduler", __name__)


@scheduler_blueprint.route("/scheduler/alerts", methods=['GET', 'POST'])
@jwt_required()
@check_scheduler_role()
def get_full_dn_list():
    if request.method == 'GET':
        dn_list = DomainName.full_list()
        return dn_full_list_view(dn_list)

    elif request.method == 'POST':
        username = get_jwt_identity()
        dn_list = DomainName.list_recent_changes(username, 1, "", "domainName", "domainName", 25)

        alert_all(dn_list)
        return valid_view("alerts are being sent")


@scheduler_blueprint.route("/scheduler/dn/<domain_name>", methods=['PUT'])
@jwt_required()
@check_scheduler_role()
def update_dn(domain_name):
    if request.method == 'PUT':
        # use the same workflow as for the user
        return put(domain_name)
        
