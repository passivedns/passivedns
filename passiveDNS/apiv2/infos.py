from fastapi import APIRouter

from passiveDNS.utils import config

infos_router = APIRouter()


@infos_router.get("/infos")
def get_infos():
    return {
        "version": config.g.VERSION,
        "job_url": config.g.JOB_URL,
        "commit_sha": config.g.COMMIT_SHA,
    }
