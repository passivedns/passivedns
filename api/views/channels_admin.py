from typing import List

from flask import jsonify

from models.channel import Channel


def ch_admin_list_view(ch_list: List[Channel]):
    ch_list_json = [ch.json() for ch in ch_list]
    ch_list_sorted = sorted(ch_list_json, key=lambda k: k['_key'])
    return jsonify({
        "msg": "channel list retrieved",
        "channel_list": ch_list_sorted
    }), 200


def ch_admin_get_view(ch: Channel):
    return jsonify({
        "msg": f"channel {ch.name} retrieved",
        "channel": ch.json()
    }), 200


def ch_admin_post_view(ch: Channel):
    return jsonify({
        "msg": f"channel {ch.name} created",
        "channel": ch.json()
    }), 200


def ch_admin_put_view(ch: Channel):
    return jsonify({
        "msg": f"channel {ch.name} updated",
        "channel": ch.json()
    }), 200


def ch_admin_delete_view(ch: Channel):
    return jsonify({
        "msg": f"channel {ch.name} deleted",
        "channel": ch.json()
    }), 200
