from datetime import datetime

import pandas
from fastapi import Response

from models.domain_name import DomainName
from models.ip_address import IPAddress
from views.misc import error_view

EXPORT_CSV = 'csv'
EXPORT_JSON = 'json'


def dn_created_view(dn: DomainName):
    return {
        "msg": "domain name created",
        "dn": dn.json()
    }, 201


def dn_modified_view(dn: DomainName):
    return {
        "msg": "domain name modified",
        "dn": dn.json()
    }, 200


def dn_retrieved_view(
        dn: DomainName,
        dn_tags: list,
        ip: IPAddress,
        ip_tags: list,
        owned: bool, followed: bool
):

    if ip is None:
        ip_json = None
    else:
        ip_json = ip.json()

    return {
        "msg": "domain name retrieved",
        "dn": dn.json(),
        "dn_tags": [t.tag for t in dn_tags],
        "ip": ip_json,
        "ip_tags": [t.tag for t in ip_tags],
        "owned": owned, "followed": followed
    }, 200


def dn_deleted_view(dn: DomainName):
    return {
        "msg": "domain name deleted",
        "dn": dn.json()
    }, 200


def dn_list_view(dn_list: list, transaction_time):
    return {
        "msg": "domain name list retrieved",
        "stats": {
            "transaction_time": transaction_time,
            "count": len(dn_list),
        },
        "dn_list": dn_list
    }, 200


def dn_list_export(dn_list: list, export):
    data = []
    for dn in dn_list:
        data.append([
            dn['domain_name'],
            dn['ip_address'],
            dn['last_ip_change'],
        ])

    columns = ['Domain name', 'IP address', 'Last IP change']
    df = pandas.DataFrame(data=data, columns=columns)

    if export == EXPORT_CSV:
        exported_data = df.to_csv(index=False)
        mimetype = "text/csv"

    elif export == EXPORT_JSON:
        exported_data = df.to_json(orient='split', index=False)
        mimetype = "application/json"

    else:
        return error_view(400, "invalid export field")

    return Response(exported_data, headers={
        "Content-Type": mimetype
    }), 200


def alert_list(dn_list: list, transaction_time):
    return {
        "msg": "domain name list retrieved",
        "stats": {
            "transaction_time": transaction_time,
            "count": len(dn_list),
        },
        "dn_list": dn_list
    }, 200


def alert_list_export(dn_list: list, export):
    data = []
    for dn in dn_list:
        data.append([
            dn['domain_name'],
            dn['domain_name_tags'],
            dn['last_ip_address'],
            dn['last_ip_tags'],
            dn['current_ip_address'],
            dn['current_ip_tags']
        ])

    columns = [
        'Domain name', 'Domain name tags', 'Last IP address', 'Last IP tags',
        'Current IP address', 'Current IP tags'
    ]
    df = pandas.DataFrame(data=data, columns=columns)
    if export == EXPORT_CSV:
        exported_data = df.to_csv(index=False)
        mimetype = "text/csv"

    elif export == EXPORT_JSON:
        exported_data = df.to_json(orient='split', index=False)
        mimetype = "application/json"

    else:
        return error_view(400, "invalid export field")

    return Response(exported_data, headers={
        "Content-Type": mimetype
    }), 200
