from operator import itemgetter

from fastapi import APIRouter, HTTPException

from models.domain_name import DomainNameResolutionError
from models.ip_address import IPAddress
from models.resolution import Resolution

resolution_router = APIRouter()


@resolution_router.get("/resolution/{domain_name}")
def get_resolutions(domain_name):
    try:
        # return the list of IPs resolved by this domain name
        r = Resolution.get_current_from_domain(domain_name)
    except DomainNameResolutionError as de:
        raise HTTPException(status_code=404, detail=str(de))

    return {"msg": "domain name resolutions retrieved", "resolution": r.json()}


@resolution_router.get("/resolution/{domain_name}/history")
def get_resolution_history(domain_name):
    out = []

    resolution_list = Resolution.list_from_domain(domain_name)
    if len(resolution_list) == 0:
        raise HTTPException(
            status_code=404, detail="no resolution found for this domain"
        )

    for resolution in resolution_list:
        ip = IPAddress.get(resolution.ip_address)
        out.append(
            {
                "first_updated_at": resolution.first_updated_at.isoformat(),
                "last_updated_at": resolution.last_updated_at.isoformat(),
                "ip": ip.json(),
                "resolver": resolution.resolver,
            }
        )
    out_sorted = sorted(out, key=itemgetter("last_updated_at"), reverse=True)
    return {"msg": "domain name resolution history retrieved", "history": out_sorted}


@resolution_router.get("/reverse/{ip_address}")
def get_reverse(ip_address):
    resolution_list = Resolution.list_from_ip(ip_address)
    if len(resolution_list) == 0:
        raise HTTPException(status_code=404, detail="no resolution found for this IP")

    return {
        "msg": "domain name resolutions retrieved",
        "resolution_list": [r.json() for r in resolution_list],
    }


@resolution_router.get("/reverse/{ip_address}/history")
def get_reverse_history(ip_address):
    out = []

    resolution_list = Resolution.list_from_ip(ip_address)
    if len(resolution_list) == 0:
        raise HTTPException(
            status_code=404, detail="no resolution reverse found for this IP"
        )

    # Adding the result in a list
    for resolution in resolution_list:
        ip = IPAddress.get(resolution.ip_address)
        out.append(
            {
                "first_updated_at": resolution.first_updated_at.isoformat(),
                "last_updated_at": resolution.last_updated_at.isoformat(),
                "ip": ip.json(),
            }
        )

    # Sorting for nice output
    out_sorted = sorted(out, key=itemgetter("last_updated_at"), reverse=True)
    return {"msg": "domain name resolution history retrieved", "history": out_sorted}
