from operator import itemgetter
from typing import List
from models.resolution import Resolution


def dn_resolutions_view(resolution: Resolution):
    return {
        "msg": f"domain name resolutions retrieved",
        "resolution": resolution.json()
    }, 200


def dn_resolutions_list_view(resolution_list: List[Resolution]):
    return {
        "msg": f"domain name resolutions retrieved",
        "resolution_list": [
            r.json() for r in resolution_list
        ]
    }, 200


def dn_resolution_history_view(out: list):
    # sort by first seen descending
    out_sorted = sorted(out, key=itemgetter('last_updated_at'), reverse=True)
    return {
        "msg": f"domain name resolution history retrieved",
        "history": out_sorted
    }
