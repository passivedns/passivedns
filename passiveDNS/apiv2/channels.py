from fastapi import APIRouter, HTTPException

from passiveDNS.utils.channels.send import test_send
from passiveDNS.models.channel import Channel
from passiveDNS.db.database import ObjectNotFound

channels_router = APIRouter()


# get the list of all available channels
@channels_router.get("/channels")
async def channels_list():
    ch_list = Channel.list()

    return {
        "msg": "available channel list retrieved",
        "channel_list": [ch.safe_json() for ch in ch_list],
    }


@channels_router.get("/channels/{channel_name}")
async def channel_get(channel_name):
    try:
        ch = Channel.get(channel_name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="channel not found")

    return {"msg": f"channel {ch.name} retrieved", "channel": ch.safe_json()}


@channels_router.get("/channel/test/{channel_name}")
async def channel_test(channel_name):
    try:
        ch = Channel.get(channel_name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="channel not found")

    test_send(ch)
    return {"msg": f"test message sent to channel {ch.name}", "channel": ch.safe_json()}
