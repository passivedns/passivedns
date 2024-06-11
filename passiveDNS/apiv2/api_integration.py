from fastapi import APIRouter, Depends, HTTPException

from apiv2.auth import get_current_user
from models.user import User
from models.domain_name import DomainName
from models.ip_address import IPAddress
from models.api_integration import APIIntegration
from analytics.extern_api import ExternAPI, VIRUSTOTAL_API, ALIENVAULT_API, MethodException, FormatException, RequestException
from db.database import ObjectNotFound

api_integration_router = APIRouter()

# get domain resolution from external api
@api_integration_router.post("/apiintegration/dn/{api_name}")
def getDomain(api_name, domain_name: str, user: User = Depends(get_current_user)):
    #check domain exists
    try:
        domain = DomainName.get(domain_name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail=f"Domain name {domain_name} not found")
    
    #check api exists
    try:
        api = APIIntegration.get(api_name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Extern API not found")

    #check user has key for it
    user_key = user.api_keys[api_name]
    if user_key == "":
        raise HTTPException(status_code=404, detail="User key not found")

    #try request
    try:
        response = ExternAPI(api, user_key).requestDomain(domain)
    except FormatException:
        raise HTTPException(status_code=422, detail="The domain is not valid")
    except MethodException as m:
        raise HTTPException(status_code=422, detail=f"The method {m} is not supported")
    except RequestException as r:
        raise HTTPException(status_code=r.status_code, detail=f"Error : {r.message}")
    
    #if api_name == VIRUSTOTAL_API:
        #treat virustotal response : "data":[{"ip_address":..., "resolver":...},...]

    #elif api_name == ALIENVAULT_API:
        #treat alienvault response : "passive_dns" : [{"address":..., },...]
    
    #get existing data (domain, ip, resolution) and update it
    
    
    return {
        "msg":"Domain name resolved and updated",
        "request_response":response
    }

@api_integration_router.post("/apiintegration/ip/{api_name}")
def getIP(api_name, ip_address: str, user: User = Depends(get_current_user)):
    #check ip exists
    try:
        ip = IPAddress.get(ip_address)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail=f"IP address {ip_address} not found")
    
    #check api exists
    try:
        api = APIIntegration.get(api_name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Extern API not found")

    #check user has key for it
    user_key = user.api_keys[api_name]
    if user_key == "":
        raise HTTPException(status_code=404, detail="User key not found")

    #try request
    try:
        response = ExternAPI(api, user_key).requestIP(ip)
    except FormatException:
        raise HTTPException(status_code=422, detail="The ip is not valid")
    except MethodException as m:
        raise HTTPException(status_code=422, detail=f"The method {m} is not supported")
    except RequestException as r:
        raise HTTPException(status_code=r.status_code, detail=f"Error : {r.message}")
    
    #if api_name == VIRUSTOTAL_API:
        #treat virustotal response : "data":[{"host_name":..., "resolver":...},...]

    #elif api_name == ALIENVAULT_API:
        #treat alienvault response : "passive_dns" : [{"hostname":..., },...]
    
    #get existing data (domain, ip, resolution) and update it
    
    
    return {
        "msg":"IP address resolved and updated",
        "request_response":response
    }