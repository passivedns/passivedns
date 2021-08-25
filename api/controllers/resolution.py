from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from controllers.utils import check_admin_user_role
from models.domain_name import DomainNameResolutionError
from models.ip_address import IPAddress
from models.resolution import Resolution
from views.misc import error_view
from views.resolution import *

resolution_blueprint = Blueprint("resolution", __name__)


@resolution_blueprint.route(
    "/resolution/<domain_name>", methods=['GET']
)
@jwt_required()
@check_admin_user_role()
def get_resolutions(domain_name):
    if request.method == 'GET':
        try:
            # return the list of IPs resolved by this domain name
            r = Resolution.get_current_from_domain(domain_name)
            return dn_resolutions_view(r)
        except DomainNameResolutionError as de:
            return error_view(404, str(de))


@resolution_blueprint.route(
    "/resolution/<domain_name>/history", methods=['GET']
)
@jwt_required()
@check_admin_user_role()
def get_resolution_history(domain_name):
    if request.method == 'GET':
        out = []

        resolution_list = Resolution.list_from_domain(domain_name)
            
        for resolution in resolution_list:
            ip = IPAddress.get(resolution.ip_address)
            out.append({
                "first_updated_at": resolution.first_updated_at.isoformat(),
                "last_updated_at": resolution.last_updated_at.isoformat(),
                "ip": ip.json()
            })
        return dn_resolution_history_view(out)


@resolution_blueprint.route(
    "/reverse/<ip_address>", methods=['GET']
)
@jwt_required()
@check_admin_user_role()
def get_reverse(ip_address):
    if request.method == 'GET':
        resolution_list = Resolution.list_from_ip(ip_address)
        if len(resolution_list) == 0:
            return error_view(404, "no resolution found for this IP")

        return dn_resolutions_list_view(resolution_list)


@resolution_blueprint.route("/reverse/<ip_address>/history", methods=['GET'])
@jwt_required()
@check_admin_user_role()
def get_reverse_history(ip_address):
    if request.method == 'GET':
        resolution_list = Resolution.list_from_ip(ip_address)       
        if len(resolution_list) == 0:       
            return error_view(404, "no resolution reverse found for this IP")       
        return dn_resolution_history_view(resolution_list)