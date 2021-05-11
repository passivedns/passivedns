from typing import List

from flask import jsonify

from models.channel import Channel


def ch_list_view(ch_list: List[Channel]):
    return jsonify({
        "msg": "available channel list retrieved",
        "channel_list": [
            ch.safe_json() for ch in ch_list
        ]
    }), 200


def ch_get_view(ch: Channel):
    return jsonify({
        "msg": f"channel {ch.name} retrieved",
        "channel": ch.safe_json()
    }), 200

