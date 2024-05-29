from fastapi import APIRouter, HTTPException

from models.tag import Tag
from models.tag_dn_ip import TagDnIP

tag_router = APIRouter()


@tag_router.post("/tag/{tag_name}")
def create_tag(tag_name):
    if Tag.exists(tag_name):
        raise HTTPException(status_code=500, detail="tag already exists")

    new_tag = Tag.new(tag_name)
    new_tag.insert()

    return {
        "msg": f"tag {new_tag.name} created",
    }


@tag_router.delete("/tag/{tag_name}")
def delete_tag(tag_name):
    if not Tag.exists(tag_name):
        raise HTTPException(status_code=404, detail="tag not found")

    tag = Tag.get(tag_name)
    tag.delete()

    tag_links = TagDnIP.list_from_tag(tag.name)
    for t in tag_links:
        t.delete()

    return {
        "msg": f"tag {tag.name} deleted",
    }


@tag_router.get("/tag")
def get_tag_list():
    return {
        "msg": "tag list retrieved",
        "tag_list": [t.json()["_key"] for t in Tag.list()],
    }
