import os
from datetime import timedelta

from fastapi import APIRouter, FastAPI, Depends
from starlette.middleware.sessions import SessionMiddleware

from utils import config
config.init_config()

from apiv2.alert import alert_router
from apiv2.auth import auth_router, get_current_user, check_admin_role, check_admin_user_role
#from api.channels import channels_router
#from api.channels_admin import channels_admin_router
from apiv2.domain_name import domain_name_router
#from api.infos import infos_router
#from api.resolution import resolution_router
#from api.scheduler import scheduler_router
#from api.scheduler_admin import scheduler_admin_router
#from api.tag import tag_router
#from api.tag_dn_ip import tag_dn_ip_router
#from api.user_channel import users_channel_router
from apiv2.users import users_router
from apiv2.users_admin import users_admin_router

# global setup
from utils.timezone import check_timezone


check_timezone(config.g.TIMEZONE)

# app setup
app = FastAPI(title="Passive DNS API")
app.add_middleware(SessionMiddleware, secret_key=config.g.JWT_SECRET_KEY)


app.access_token_expires = timedelta(hours=1)

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(users_admin_router, dependencies=[Depends(get_current_user), Depends(check_admin_role)])
api_router.include_router(domain_name_router, dependencies=[Depends(get_current_user)])
#api_router.include_router(resolution_router)
#api_router.include_router(scheduler_router)
#api_router.include_router(scheduler_admin_router)
#api_router.include_router(channels_router)
#api_router.include_router(channels_admin_router)
#api_router.include_router(users_channel_router)
#api_router.include_router(tag_router)
#api_router.include_router(tag_dn_ip_router)
api_router.include_router(alert_router, dependencies=[Depends(get_current_user), Depends(check_admin_user_role)])

#api_router.include_router(infos_router)

app.include_router(api_router, prefix="/api/v2")

debug = config.g.DEBUG == "1"

#à la main avec poetry après
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
