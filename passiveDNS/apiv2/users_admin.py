from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from passiveDNS.db.database import ObjectNotFound
from passiveDNS.models.user import User, UserRole

users_admin_router = APIRouter()

class CreateUser(BaseModel):
    password: str

# the list of the users registered
# require admin JWT
@users_admin_router.get("/admin/users/list")
async def get_user_list():
    user_list = User.list()
    return {
        "msg": "user list retrieved",
        "user_list": [u.safe_json() for u in user_list],
    }


# remove a user
# require admin JWT
@users_admin_router.delete("/admin/users/{username}")
async def remove_user(username):
    try:
        user = User.get(username)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="user not found")

    if user.role != UserRole.ADMIN.value:
        user.delete()

        return {"msg": f"user {user.username} deleted", "user": user.safe_json()}

    else:
        raise HTTPException(status_code=500, detail="cannot remove an admin user")


# create a user
# require admin JWT
@users_admin_router.post("/admin/users/{username}")
async def verify_requested_user(username, user_data: CreateUser):
    
    if User.exists(username):
        raise HTTPException(status_code=500, detail="name unavailable")

    new_user = User.new(
        username, user_data.password
    )
    new_user.insert()

    return {"msg": "user created", "user": new_user.safe_json()}
