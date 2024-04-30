from models.user import User


def scheduler_created_view(user: User):
    return {
        "msg": "scheduler user created",
        "scheduler": user.safe_json()
    }, 201


def scheduler_updated_view(user: User):
    return {
        "msg": "scheduler user updated",
        "scheduler": user.safe_json()
    }, 200


def scheduler_deleted_view(user: User):
    return {
        "msg": "scheduler user deleted",
        "scheduler": user.safe_json()
    }, 200


def dn_full_list_view(dn_list):
    return {
        "msg": "full domain name list retrieved",
        "dn_list": dn_list
    }, 200
