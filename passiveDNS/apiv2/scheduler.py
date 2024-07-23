from fastapi import APIRouter, Depends, HTTPException
from defang import refang
import validators
from passiveDNS.utils.channels.send import alert_all_dn
from passiveDNS.apiv2.auth import get_current_user
from passiveDNS.models.domain_name import (
    DomainName,
    DomainNameFilterNotFound,
    DomainNameSortNotFound,
)
from passiveDNS.models.ip_address import IPAddress
from passiveDNS.models.resolution import Resolution
from passiveDNS.models.user import User
from passiveDNS.db.database import ObjectNotFound

scheduler_router = APIRouter()


@scheduler_router.get("/scheduler/alerts")
async def get_full_dn_list():
    dn_list = DomainName.full_list()
    return {"msg": "full domain name list retrieved", "dn_list": dn_list}


@scheduler_router.put("/scheduler/dn/{domain_name}")
async def update_dn_alert(domain_name):
    domain_name = refang(domain_name)
    if not validators.domain(domain_name):
        raise HTTPException(status_code=500, detail="domain name not valid")

    try:
        dn = DomainName.get(domain_name)
    except ObjectNotFound as o:
        raise HTTPException(status_code=404, detail=str(o))

    ip_address = dn.resolve()
    if ip_address is None:
        raise HTTPException(status_code=404, detail="could not resolve domain name")

    if not IPAddress.exists(ip_address):
        # the DN resolves a new address
        ip = IPAddress.new(ip_address)
        ip.insert()

    if not Resolution.exists(domain_name, ip_address):
        # ip change detected
        domain_alert = {
            "domain_name": domain_name,
            "last_ip_address": Resolution.get_current_from_domain(domain_name),
            "current_ip_address": ip_address,
        }
        resolution = Resolution.new(domain_name, ip_address, "PassiveDNS")
        resolution.insert()
        alert_all_dn(domain_alert)

    else:
        resolution = Resolution.get(domain_name, ip_address)
        resolution.update()

    dn.update()
    return {"msg": "domain name modified", "dn": dn.json()}
