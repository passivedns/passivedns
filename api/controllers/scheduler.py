from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from channels.send import alert_all
from controllers.utils import check_scheduler_role
from views.misc import valid_view
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
        dn_list = DomainName.list_recent_changes(1, "", "", "domainName", 25)

        alert_all(dn_list)
        return valid_view("alerts are being sent")
