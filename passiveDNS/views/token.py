
def token_view(token):
    return {
        "access_token": token,
        "token_type": "bearer"
    }, 200
