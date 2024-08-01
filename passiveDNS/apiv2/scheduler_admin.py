from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from passiveDNS.apiv2.auth import get_current_user
from passiveDNS.models.user import User

scheduler_admin_router = APIRouter()


class PasswordJson(BaseModel):
    password: str


@scheduler_admin_router.post("/admin/scheduler/{scheduler_name}")
async def create_scheduler(scheduler_name, data: PasswordJson):
    if User.exists(scheduler_name):
        raise HTTPException(status_code=500, detail="name unavailable")

    new_scheduler = User.new(scheduler_name, data.password, is_scheduler=True)
    new_scheduler.insert()

    return {"msg": "scheduler user created", "scheduler": new_scheduler.safe_json()}


@scheduler_admin_router.put("/admin/scheduler/{scheduler_name}")
async def update_scheduler(scheduler_name, data: PasswordJson):
    if not User.exists(scheduler_name):
        raise HTTPException(status_code=404, detail="scheduler not found")

    scheduler = User.get(scheduler_name)
    scheduler.update_password(data.password)

    return {"msg": "scheduler user updated", "scheduler": scheduler.safe_json()}
