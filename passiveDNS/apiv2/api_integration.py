from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import validators

from passiveDNS.apiv2.auth import get_current_user
from passiveDNS.models.user import User
from passiveDNS.models.domain_name import DomainName
from passiveDNS.models.ip_address import IPAddress
from passiveDNS.models.resolution import Resolution
from passiveDNS.models.api_integration import APIIntegration
from passiveDNS.analytics.extern_api import (
    ExternAPI,
    MethodException,
    FormatException,
    RequestException,
)
from passiveDNS.db.database import ObjectNotFound

api_integration_router = APIRouter()

# Tests for this controller have to be done manually since it needs a personal apikey

class APIData(BaseModel):
    base_url: str
    header: str
    ip_method: str
    ip_uri: str
    domain_method: str
    domain_uri: str


@api_integration_router.put("/apiintegration/{api_name}")
def updateApi(api_name, data: APIData):
    #check api exists
    try:
        api = APIIntegration.get(api_name)
    except ObjectNotFound:
        raise HTTPException(
            status_code=404, detail=f"API {api_name} not found"
        )

    api.base_url = data.base_url
    api.header = data.header
    api.ip_method = data.ip_method
    api.ip_uri = data.ip_uri
    api.domain_method = data.domain_method
    api.domain_uri = data.domain_uri
    api.update()

    return {
        "msg":f"API {api_name} successfully updated"
    }

# get domain resolution from external api
@api_integration_router.post("/apiintegration/dn/{api_name}")
def getDomain(api_name, domain_name: str, user: User = Depends(get_current_user)):
    # check domain exists
    try:
        domain = DomainName.get(domain_name)
    except ObjectNotFound:
        raise HTTPException(
            status_code=404, detail=f"Domain name {domain_name} not found"
        )

    # check api exists
    try:
        api = APIIntegration.get(api_name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Extern API not found")

    # check user has key for it
    user_key = user.api_keys[api_name]
    if user_key == "":
        raise HTTPException(status_code=404, detail="User key not found")

    # try request
    try:
        response = ExternAPI(api, user_key).requestDomain(domain)
    except FormatException:
        raise HTTPException(status_code=422, detail="The domain is not valid")
    except MethodException as m:
        raise HTTPException(status_code=422, detail=f"The method {m} is not supported")
    except RequestException as r:
        raise HTTPException(status_code=r.status_code, detail=f"Error : {r.message}")

    # create new ip and resolution
    count_new = 0
    count_update = 0
    for data in response:
        ip = data["ip_address"]
        # check ip is IPv4 format
        if validators.ipv4(ip):
            # check if ip exists in DB
            if IPAddress.exists(ip):
                # check if resolution exists in DB
                if Resolution.exists(domain_name, ip):
                    res_tmp = Resolution.get(domain_name, ip)
                    res_tmp.resolver = api_name
                    res_tmp.update()
                    count_update += 1
                else:
                    res_tmp = Resolution.new(
                        domain_name,
                        ip,
                        api_name,
                        first_updated=data["first_updated_at"],
                        last_updated=data["last_updated_at"],
                    )
                    res_tmp.insert()
                    count_new += 1
            else:
                # create ip and resolution
                ip_tmp = IPAddress.new(ip)
                ip_tmp.insert()

                res_tmp = Resolution.new(
                    domain_name,
                    ip,
                    api_name,
                    first_updated=data["first_updated_at"],
                    last_updated=data["last_updated_at"],
                )
                res_tmp.insert()
                count_new += 1

    return {
        "msg": "Domain name resolved",
        "Resolution added": count_new,
        "Resolution updated": count_update,
    }


@api_integration_router.post("/apiintegration/ip/{api_name}")
def getIP(api_name, ip_address: str, user: User = Depends(get_current_user)):
    # check ip exists
    try:
        ip = IPAddress.get(ip_address)
    except ObjectNotFound:
        raise HTTPException(
            status_code=404, detail=f"IP address {ip_address} not found"
        )

    # check api exists
    try:
        api = APIIntegration.get(api_name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Extern API not found")

    # check user has key for it
    user_key = user.api_keys[api_name]
    if user_key == "":
        raise HTTPException(status_code=404, detail="User key not found")

    # try request
    try:
        response = ExternAPI(api, user_key).requestIP(ip)
    except FormatException:
        raise HTTPException(status_code=422, detail="The ip is not valid")
    except MethodException as m:
        raise HTTPException(status_code=422, detail=f"The method {m} is not supported")
    except RequestException as r:
        raise HTTPException(status_code=r.status_code, detail=f"Error : {r.message}")

    # create new domain and resolution
    count_new = 0
    count_update = 0
    for data in response:
        domain = data["domain_name"]
        # check ip is domain format
        if validators.domain(domain):
            # check if domain exists in DB
            if DomainName.exists(domain):
                # check if resolution exists in DB
                if Resolution.exists(domain, ip_address):
                    res_tmp = Resolution.get(domain, ip_address)
                    res_tmp.resolver = api_name
                    res_tmp.update()
                    count_update += 1
                else:
                    res_tmp = Resolution.new(
                        domain,
                        ip_address,
                        api_name,
                        first_updated=data["first_updated_at"],
                        last_updated=data["last_updated_at"],
                    )
                    res_tmp.insert()
                    count_new += 1

            else:
                # create domain and resolution
                domain_tmp = DomainName.new(domain)
                domain_tmp.insert()

                res_tmp = Resolution.new(
                    domain,
                    ip_address,
                    api_name,
                    first_updated=data.first_updated_at,
                    last_updated=data.last_updated_at,
                )
                res_tmp.insert()
                count_new += 1

    return {
        "msg": "IP address resolved",
        "Resolution added": count_new,
        "Resolution updated": count_update,
    }


@api_integration_router.get("/apiintegration")
def api_integration_list(user: User = Depends(get_current_user)):
    """
    The list of available apis for a user
    """
    api_list = APIIntegration.list()

    available_apis = []
    for api in api_list:
        if api.name not in user.api_keys:
            available_apis.append(api)

    return {"msg": "Available apis retrived", "api_list": available_apis}


@api_integration_router.get("/user/apiintegration")
def api_integration_user_list(user: User = Depends(get_current_user)):
    """
    The list of linked apis for a user
    """
    api_list = APIIntegration.list()

    available_apis = []
    for api in api_list:
        if api.name in user.api_keys:
            available_apis.append(api)

    return {"msg": "Linked apis retrived", "api_list": available_apis}
