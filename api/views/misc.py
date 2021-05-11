from flask import jsonify


def error_view(code, message):
    return jsonify({
        "msg": message
    }), code


def valid_view(message):
    return jsonify({
        "msg": message
    }), 200
