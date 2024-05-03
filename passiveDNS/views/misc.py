
def error_view(code, message):
    return {
        "msg": message
    }, code


def valid_view(message):
    return {
        "msg": message
    }, 200
