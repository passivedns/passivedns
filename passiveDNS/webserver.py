from datetime import timedelta

from fastapi import APIRouter, FastAPI, Depends
from starlette.middleware.sessions import SessionMiddleware


from passiveDNS.utils import config


config.init_config()

from passiveDNS.apiv2.alert import alert_router  # noqa: E402
from passiveDNS.apiv2.auth import (  # noqa: E402
    auth_router,
    get_current_user,
    check_admin_role,
    check_admin_user_role,
    check_scheduler_role,
)
from passiveDNS.apiv2.channels import channels_router  # noqa: E402
from passiveDNS.apiv2.channels_admin import channels_admin_router  # noqa: E402
from passiveDNS.apiv2.domain_name import domain_name_router  # noqa: E402
from passiveDNS.apiv2.infos import infos_router  # noqa: E402
from passiveDNS.apiv2.resolution import resolution_router  # noqa: E402
from passiveDNS.apiv2.scheduler import scheduler_router  # noqa: E402
from passiveDNS.apiv2.scheduler_admin import scheduler_admin_router  # noqa: E402
from passiveDNS.apiv2.tag import tag_router  # noqa: E402
from passiveDNS.apiv2.tag_dn_ip import tag_dn_ip_router  # noqa: E402
from passiveDNS.apiv2.users import users_router  # noqa: E402
from passiveDNS.apiv2.users_admin import users_admin_router  # noqa: E402
from passiveDNS.apiv2.api_integration import api_integration_router  # noqa: E402

# global setup
from passiveDNS.utils.timezone import check_timezone  # noqa: E402


check_timezone(config.g.TIMEZONE)

# app setup
app = FastAPI(title="Passive DNS API")
app.add_middleware(SessionMiddleware, secret_key=config.g.JWT_SECRET_KEY)


app.access_token_expires = timedelta(hours=1)

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(
    users_admin_router,
    dependencies=[Depends(get_current_user), Depends(check_admin_role)],
)
api_router.include_router(
    domain_name_router,
    dependencies=[Depends(get_current_user), Depends(check_admin_user_role)],
)
api_router.include_router(
    resolution_router,
    dependencies=[Depends(get_current_user), Depends(check_admin_user_role)],
)
api_router.include_router(
    scheduler_router,
    dependencies=[Depends(get_current_user), Depends(check_scheduler_role)],
)
api_router.include_router(
    scheduler_admin_router,
    dependencies=[Depends(get_current_user), Depends(check_admin_role)],
)
api_router.include_router(
    channels_router,
    dependencies=[Depends(get_current_user), Depends(check_admin_user_role)],
)
api_router.include_router(
    channels_admin_router,
    dependencies=[Depends(get_current_user), Depends(check_admin_role)],
)
api_router.include_router(
    tag_router, dependencies=[Depends(get_current_user), Depends(check_admin_user_role)]
)
api_router.include_router(
    tag_dn_ip_router,
    dependencies=[Depends(get_current_user), Depends(check_admin_user_role)],
)
api_router.include_router(
    alert_router,
    dependencies=[Depends(get_current_user), Depends(check_admin_user_role)],
)
api_router.include_router(
    api_integration_router,
    dependencies=[Depends(get_current_user), Depends(check_admin_user_role)],
)

api_router.include_router(infos_router)

app.include_router(api_router, prefix="/apiv2")

debug = config.g.DEBUG == "1"
