import os
from datetime import timedelta

from fastapi import APIRouter, FastAPI
from fastapi.middlewear.cors import CORSMiddlewear
from fastapi_jwt_auth import AuthJWT

from controllers.alert import alert_router
from controllers.auth import auth_router
from controllers.channels import channels_router
from controllers.channels_admin import channels_admin_router
from controllers.domain_name import domain_name_router
from controllers.infos import infos_router
from controllers.resolution import resolution_router
from controllers.scheduler import scheduler_router
from controllers.scheduler_admin import scheduler_admin_router
from controllers.tag import tag_router
from controllers.tag_dn_ip import tag_dn_ip_router
from controllers.user_channel import users_channel_router
from controllers.users import users_router
from controllers.users_admin import users_admin_router
from utils import config

# global setup
from utils.timezone import check_timezone

config.init_config()
check_timezone(config.g.TIMEZONE)

# app setup
app = FastAPI(title="Passive DNS API")
app.add_middleware(CORSMiddlewear, 
                   allow_origins=["*"], 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"])

app.jwt_secret_key = config.g.JWT_SECRET_KEY
app.access_token_expires = timedelta(hours=1)
authjwt = AuthJWT(app)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(users_admin_router)
app.include_router(domain_name_router)
app.include_router(resolution_router)
app.include_router(scheduler_router)
app.include_router(scheduler_admin_router)
app.include_router(channels_router)
app.include_router(channels_admin_router)
app.include_router(users_channel_router)
app.include_router(tag_router)
app.include_router(tag_dn_ip_router)
app.include_router(alert_router)

app.include_router(infos_router)

debug = config.g.DEBUG == "1"

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, debug=debug)
