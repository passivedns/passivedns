from time import time

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.utils import check_admin_user_role
from models.domain_name import DomainNameFilterNotFound, DomainNameSortNotFound, DomainName
from views.domain_name import alert_list_export, alert_list
from views.misc import error_view

alert_blueprint = Blueprint("alert", __name__)


def get_list():
    try:
        username = get_jwt_identity()

        input_filter = request.args.get('filter')
        input_filter_by = request.args.get('filter_by')
        sort_by = request.args.get('sort_by')
        limit_str = request.args.get('limit')
        days_str = request.args.get('days')

        export = request.args.get('export')

        params = [input_filter, input_filter_by, sort_by, limit_str, days_str]
        for p in params:
            if p is None:
                return error_view(400, 'missing parameter')

        if not limit_str.isdigit():
            return error_view(400, 'invalid limit')

        if not days_str.isdigit():
            return error_view(400, 'invalid days count')

        limit = int(limit_str)
        days = int(days_str)

        t1 = time()
        dn_list = DomainName.list_recent_changes(
            username, days, input_filter, input_filter_by, sort_by, limit
        )
        t2 = time()
        transaction_time = round(t2 - t1, 2)

        if export is not None and export != '':
            return alert_list_export(dn_list, export)
        else:
            return alert_list(dn_list, transaction_time)

    except DomainNameFilterNotFound:
        return error_view(400, "invalid filter field")

    except DomainNameSortNotFound:
        return error_view(400, "invalid sort field")


@alert_blueprint.route("/alert", methods=['GET'])
@jwt_required()
@check_admin_user_role()
def manage_alert():
    if request.method == 'GET':
        return get_list()
