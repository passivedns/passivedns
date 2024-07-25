from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from passiveDNS.db.database import ObjectNotFound
from passiveDNS.models.user import User
from passiveDNS.models.api_integration import APIIntegration
from passiveDNS.analytics.extern_api import ExternAPI, RequestException

from passiveDNS.apiv2.auth import get_current_user

users_router = APIRouter()

class ChangePassword(BaseModel):
    current_password: str
    new_password: str

@users_router.put("/password", dependencies=[Depends(get_current_user)])
async def change_password(
    password_data: ChangePassword, current_user: User = Depends(get_current_user)
):
    current_password = password_data.current_password
    new_password = password_data.new_password

    username = current_user.username
    user = User.get(username)
    if not user.verify_password(current_password):
        raise HTTPException(status_code=401, detail="invalid password")

    if new_password == current_password:
        raise HTTPException(status_code=400, detail="new password same as current")

    user.update_password(new_password)

    return {"msg": "password changed"}


@users_router.post("/apikey/{api_name}", dependencies=[Depends(get_current_user)])
async def add_api_key(api_name, api_key: str, user: User = Depends(get_current_user)):
    # check api exists
    try:
        api = APIIntegration.get(api_name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Extern API not found")

    # check key is valid
    try:
        ExternAPI(api, api_key).testRequest()
    except RequestException as r:
        raise HTTPException(status_code=r.status_code, detail=f"Error : {r.message}")

    user.update_api_keys(api_name, api_key)

    return {"msg": f"Key for api {api_name} added to user {user.username}"}


@users_router.delete("/apikey/{api_name}", dependencies=[Depends(get_current_user)])
async def remove_api_key(api_name, user: User = Depends(get_current_user)):
    # check api exists
    try:
        APIIntegration.get(api_name)
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail="Extern API not found")

    # check key is valid
    api = user.api_keys[api_name]
    if api is None:
        raise HTTPException(
            status_code=404,
            detail=f"Error : This user does not have an api key linked to {api_name}",
        )

    user.remove_api_key(api_name)

    return {"msg": f"Key for api {api_name} removed from user {user.username}"}
