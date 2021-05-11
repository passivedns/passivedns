from flask import jsonify


def tag_link_created_view(tag_link):
    return jsonify({
        "msg": "tag link created",
        "tag_link": tag_link.json()
    }), 201


def tag_link_deleted_view(tag_link):
    return jsonify({
        "msg": "tag link deleted",
        "tag_link": tag_link.json()
    }), 200


def tag_link_list_view(tag_link_list):
    return jsonify({
        "msg": "tag link list retrieved",
        "tag_link_list": [
            t.json()['tag'] for t in tag_link_list
        ]
    }), 200
