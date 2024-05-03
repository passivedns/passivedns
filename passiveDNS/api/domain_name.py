from time import time

from defang import refang
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.utils import check_admin_user_role
from views.domain_name import *
from views.misc import error_view, valid_view
from db.database import ObjectNotFound
from models.domain_name import DomainNameResolutionError, DomainNameFilterNotFound, DomainNameSortNotFound,\
    DOMAIN_NAME_COLLECTION
from models.ip_address import IPAddress, IP_ADDRESS_COLLECTION
from models.resolution import Resolution
from models.tag_dn_ip import TagDnIP
from models.users_dn import UserDn

domain_name_blueprint = Blueprint("domain_name", __name__)


@domain_name_blueprint.route(
    "/dn", methods=['GET']
)
@jwt_required()
@check_admin_user_role()
def manage_domain_name_list():
    if request.method == 'GET':
        try:
            username = get_jwt_identity()

            input_filter = request.args.get('filter')
            input_filter_by = request.args.get('filter_by')
            sort_by = request.args.get('sort_by')
            limit_str = request.args.get('limit')

            export = request.args.get('export')
            owned_filter = request.args.get('owned') is not None
            followed_filter = request.args.get('followed') is not None

            params = [input_filter, input_filter_by, sort_by, limit_str]
            for p in params:
                if p is None:
                    return error_view(400, 'missing parameter')

            if not limit_str.isdigit():
                return error_view(400, 'invalid limit')

            limit = int(limit_str)

            t1 = time()
            dn_list = DomainName.list(
                username, input_filter, input_filter_by,
                owned_filter, followed_filter,
                sort_by, limit
            )
            t2 = time()
            transaction_time = round(t2 - t1, 2)

            if export is not None and export != '':
                # export file data
                return dn_list_export(dn_list, export)
            else:
                # export json data
                return dn_list_view(dn_list, transaction_time)

        except DomainNameFilterNotFound:
            return error_view(400, "invalid filter field")

        except DomainNameSortNotFound:
            return error_view(400, "invalid sort field")


def post(domain_name):
    try:
        if DomainName.exists(domain_name):
            return error_view(500, f"domain name {domain_name} already exists")

        dn = DomainName.new(domain_name)
        dn.insert()

        ip_address = dn.resolve()

        # in case resolutions went fine
        if ip_address is not None:
            if not IPAddress.exists(ip_address):
                ip = IPAddress.new(ip_address)
                ip.insert()

            resolution = Resolution.new(domain_name, ip_address)
            resolution.insert()

        # create user link
        username = get_jwt_identity()
        user_dn = UserDn.new(username, dn.domain_name, True)
        user_dn.insert()

        return dn_created_view(dn)

    except DomainNameResolutionError as dre:
        return error_view(500, str(dre))


def get(domain_name):
    dn = None
    dn_tags = []
    owned = False
    followed = False

    username = get_jwt_identity()
    try:
        dn = DomainName.get(domain_name)
        dn_tags = TagDnIP.list_tags_from_object(
            dn.domain_name, DOMAIN_NAME_COLLECTION)

        if not UserDn.exists(username, domain_name):
            owned = False
            followed = False
        else:
            user_dn = UserDn.get(username, domain_name)
            owned = user_dn.owned
            followed = True

        resolution = Resolution.get_current_from_domain(dn.domain_name)

        ip = IPAddress.get(resolution.ip_address)
        ip_tags = TagDnIP.list_tags_from_object(ip.address, IP_ADDRESS_COLLECTION)

        return dn_retrieved_view(dn, dn_tags, ip, ip_tags, owned, followed)

    except ObjectNotFound as o:
        return error_view(404, str(o))

    except DomainNameResolutionError:
        return dn_retrieved_view(dn, dn_tags, None, [], owned, followed)


def put(domain_name):
    try:
        dn = DomainName.get(domain_name)
        ip_address = dn.resolve()
        if ip_address is None:
            return error_view(404, "resolution not found")

        if not IPAddress.exists(ip_address):
            # the DN resolves a new address
            ip = IPAddress.new(ip_address)
            ip.insert()

        if not Resolution.exists(domain_name, ip_address):
            # ip change detected
            resolution = Resolution.new(domain_name, ip_address)
            resolution.insert()

        else:
            resolution = Resolution.get(domain_name, ip_address)
            resolution.update()

        dn.update()
        return dn_modified_view(dn)

    except ObjectNotFound as o:
        return error_view(404, str(o))

    except DomainNameResolutionError as dre:
        return error_view(500, str(dre))


def delete(domain_name):
    try:
        username = get_jwt_identity()
        if not UserDn.exists(username, domain_name):
            return error_view(403, "no ownership found")

        # remove ownership
        user_dn = UserDn.get(username, domain_name)
        if not user_dn.owned:
            return error_view(403, "you do not own this domain")

        user_dn.delete()

        # remove tags
        dn_linked_tags = TagDnIP.list_tags_from_object(
            domain_name, DOMAIN_NAME_COLLECTION)
        for t in dn_linked_tags:
            t.delete()

        # remove resolution / IP
        resolution_list = Resolution.list_from_domain(domain_name)
        for r in resolution_list:
            r.delete()

            ip_address = r.ip_address
            res_ip_list = Resolution.list_from_ip(ip_address)
            if len(res_ip_list) == 0:
                ip_linked_tags = TagDnIP.list_tags_from_object(
                    ip_address, IP_ADDRESS_COLLECTION)
                for t in ip_linked_tags:
                    t.delete()

                ip = IPAddress.get(ip_address)
                ip.delete()

        dn = DomainName.get(domain_name)
        dn.delete()

        return dn_deleted_view(dn)
    except ObjectNotFound as o:
        return error_view(404, str(o))


@domain_name_blueprint.route(
    "/dn/<domain_name>", methods=['POST', 'PUT', 'GET', 'DELETE']
)
@jwt_required()
@check_admin_user_role()
def manage_domain_name(domain_name):
    domain_name = refang(domain_name)

    if request.method == 'POST':
        return post(domain_name)

    elif request.method == 'GET':
        return get(domain_name)

    elif request.method == 'PUT':
        return put(domain_name)

    elif request.method == 'DELETE':
        return delete(domain_name)


@domain_name_blueprint.route(
    "/dn/<domain_name>/follow", methods=['POST', 'DELETE']
)
@jwt_required()
@check_admin_user_role()
def manage_follow(domain_name):
    domain_name = refang(domain_name)
    username = get_jwt_identity()

    if request.method == 'POST':
        if UserDn.exists(username, domain_name):
            return error_view(500, "you are already following this DN")

        user_dn = UserDn.new(username, domain_name, False)
        user_dn.insert()
        return valid_view("DN added to your follows")

    elif request.method == 'DELETE':
        if not UserDn.exists(username, domain_name):
            return error_view(404, "you are not following thiS DN")

        user_dn = UserDn.get(username, domain_name)
        user_dn.delete()
        return valid_view("DN removed from your follows")
