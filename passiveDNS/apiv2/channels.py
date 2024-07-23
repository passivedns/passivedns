from fastapi import APIRouter, Depends, HTTPException

from passiveDNS.apiv2.auth import get_current_user
from passiveDNS.utils.channels.send import test_send
from passiveDNS.models.channel import Channel
from passiveDNS.models.user import User
from passiveDNS.models.user_channel import UserChannel
from passiveDNS.db.database import ObjectNotFound

channels_router = APIRouter()


# get the list of all available channels
@channels_router.get("/channels")
async def channels_list(user: User = Depends(get_current_user)):
    ch_list = Channel.list()

    username = user.username
    user_ch_list = UserChannel.list_from_username(username)

    out = []
    for ch in ch_list:
        found = False
        for u_ch in user_ch_list:
            if u_ch.channel_name == ch.name:
                found = True
                break
        if not found:
            out.append(ch)

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
    return {"msg":f"test message sent to channel {ch.name}","channel":ch.safe_json()}
