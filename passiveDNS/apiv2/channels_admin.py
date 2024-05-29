from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.channel import Channel, ChannelTypeError
from models.user_channel import UserChannel

channels_admin_router = APIRouter()


class ChannelData(BaseModel):
    type: str
    infos: dict


# get channel list - admin view
@channels_admin_router.get("/admin/channels")
def channels_admin_list():
    ch_list = Channel.list()
    # formatting and sorting for json response
    ch_list_json = [ch.json() for ch in ch_list]
    ch_list_sorted = sorted(ch_list_json, key=lambda k: k["_key"])
    return {"msg": "channel list retrieved", "channel_list": ch_list_sorted}


@channels_admin_router.post("/admin/channels/{name}")
def channel_create(name, data: ChannelData):
    ch_type = data.type
    infos = data.infos

    if Channel.exists(name):
        raise HTTPException(
            status_code=500, detail="a channel with this name already exists"
        )

    try:
        new_ch = Channel.new(name, ch_type, infos)
        new_ch.insert()

    except KeyError:
        raise HTTPException(status_code=500, detail="error parsing json input")

    except ChannelTypeError:
        raise HTTPException(status_code=400, detail="invalid channel type")

    return {"msg": f"channel {new_ch.name} created", "channel": new_ch.json()}


@channels_admin_router.get("/admin/channels/{name}")
def channel_get(name):
    if not Channel.exists(name):
        raise HTTPException(status_code=404, detail=f"channel {name} not found")

    ch = Channel.get(name)
    return {"msg": f"channel {ch.name} retrieved", "channel": ch.json()}


@channels_admin_router.put("/admin/channels/{name}")
def channel_update(name, data: ChannelData):
    infos = data.infos

    if not Channel.exists(name):
        raise HTTPException(status_code=404, detail=f"channel {name} not found")

    ch = Channel.get(name)
    ch.update(infos)

    return {"msg": f"channel {ch.name} updated", "channel": ch.json()}


@channels_admin_router.delete("/admin/channels/{name}")
def channel_delete(name):
    if name == Channel.DEFAULT:
        raise HTTPException(status_code=403, detail=f"cannot modify default channel")

    if not Channel.exists(name):
        raise HTTPException(status_code=404, detail=f"channel {name} not found")

    ch = Channel.get(name)
    user_channel_list = UserChannel.list_from_channel(ch.name)
    for user_ch in user_channel_list:
        user_ch.delete()

    ch.delete()

    return {"msg": f"channel {ch.name} deleted", "channel": ch.json()}
