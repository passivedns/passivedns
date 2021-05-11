from flask import jsonify


def tag_created_view(tag):
    return jsonify({
        "msg": f"tag {tag.name} created",
    }), 201


def tag_deleted_view(tag):
    return jsonify({
        "msg": f"tag {tag.name} deleted",
    }), 200


def tag_list_view(tag_list):
    return jsonify({
        "msg": f"tag list retrieved",
        "tag_list": [
            t.json()['_key'] for t in tag_list
        ]
    }), 200
