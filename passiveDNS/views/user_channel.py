from models.user_channel import UserChannel


def user_ch_list_view(ch_list: list):
    # return the list of channels edges and their corresponding channel
    out = [
        {
            "user_channel": o['user_channel'].safe_json(),
            "channel": o['channel'].safe_json()
        }
        for o in ch_list
    ]

    return {
        "msg": "user linked channels list retrieved",
        "channel_list": out

    }, 200


def user_ch_get_view(user_ch: UserChannel):
    return {
        "msg": f"user channel retrieved",
        "user_channel": user_ch.safe_json(),
    }


def user_ch_created_view(user_ch: UserChannel):
    return {
        "msg": f"linked channel with user {user_ch.username}",
        "user_channel": user_ch.safe_json()
    }, 201


def user_ch_updated_view(user_ch: UserChannel):
    return {
        "msg": f"channel contact verified",
        "user_channel": user_ch.safe_json()
    }, 201


def user_ch_deleted_view(user_ch: UserChannel):
    return {
        "msg": f"user channel deleted",
        "user_channel": user_ch.safe_json()
    }


def user_ch_test_view(user_ch: UserChannel):
    return {
        "msg": f"user channel tested",
        "user_channel": user_ch.safe_json()
    }
