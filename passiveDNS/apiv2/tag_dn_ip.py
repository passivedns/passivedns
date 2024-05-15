from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.tag_dn_ip import TagDnIP
from models.tag import Tag
from models.domain_name import DOMAIN_NAME_COLLECTION, DomainName
from models.ip_address import IP_ADDRESS_COLLECTION, IPAddress

tag_dn_ip_router = APIRouter()

class TagDNIP(BaseModel):
    tag: str
    object: str
    type: str

@tag_dn_ip_router.post("/tag_dn_ip")
def create_tag_dn_ip(data: TagDNIP):
    tag = data.tag
    object_key = data.object
    object_type = data.type

        
    if TagDnIP.exists(tag, object_key, object_type):
        raise HTTPException(status_code=500, detail="tag link already exists")

    if not Tag.exists(tag):
        raise HTTPException(status_code=404, detail="source tag not found")

    if object_type == DOMAIN_NAME_COLLECTION:
        object_exists = DomainName.exists(object_key)
    elif object_type == IP_ADDRESS_COLLECTION:
        object_exists = IPAddress.exists(object_key)
    else:
        raise HTTPException(status_code=400, detail="invalid object type")

    if not object_exists:
        raise HTTPException(status_code=404, detail="target object not found")

    new_tag_link = TagDnIP.new(tag, object_key, object_type)
    new_tag_link.insert()

    return {
        "msg": "tag link created",
        "tag_link": new_tag_link.json()
    }

@tag_dn_ip_router.delete("/tag_dn_ip")
def delete_tag_dn_ip(data: TagDNIP):
    tag = data.tag
    object_key = data.object
    object_type = data.type

    if not TagDnIP.exists(tag, object_key, object_type):
        raise HTTPException(status_code=404, detail="tag link not found")

    tag_link = TagDnIP.get(tag, object_key, object_type)
    tag_link.delete()

    return {
        "msg": "tag link deleted",
        "tag_link": tag_link.json()
    }

@tag_dn_ip_router.get("/tag_dn_ip/list/from")
def get_tag_dn_ip_list(object: str, type: str):
    object_key = object
    object_type = type

    tag_linked_list = TagDnIP.list_tags_from_object(object_key, object_type)
    return {
        "msg": "tag link list retrieved",
        "tag_link_list": [
            t.json()['tag'] for t in tag_linked_list
        ]
    }
