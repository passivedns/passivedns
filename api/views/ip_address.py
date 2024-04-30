from models.ip_address import IPAddress


def ip_created_view(ip: IPAddress):
    return {
        "msg": "ip address created",
        "ip": ip.json()
    }, 201


def ip_modified_view(ip: IPAddress):
    return {
        "msg": "ip address modified",
        "ip": ip.json()
    }, 200


def ip_retrieved_view(ip: IPAddress):
    return {
        "msg": "ip address retrieved",
        "ip": ip.json()
    }, 200


def ip_deleted_view(ip: IPAddress):
    return {
        "msg": "ip address deleted",
        "ip": ip.json()
    }, 200


def ip_list_view(ip_list: list):
    return {
        "msg": "ip address list retrieved",
        "ip_list": [ip.json() for ip in ip_list]
    }, 200
