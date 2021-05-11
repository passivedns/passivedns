from flask import jsonify


def token_view(token):
    return jsonify({
        "access_token": token
    }), 200
