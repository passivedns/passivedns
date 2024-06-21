import celery
from client import ApiClient
import logging
import os
import json

app = celery.Celery("tasks", broker="redis://redis:6379/0")
app.conf.beat_schedule = {
    "daily-task": {
        "task": "tasks.daily_task",
        "schedule": 86400.0,  # 24 hours in seconds
    },
}


@app.task
def resolve(client_data: dict, domain_name: str):
    client = ApiClient(**json.loads(client_data))
    logging.debug(f"resolving {domain_name}")
    logging.debug(f"client: {client}")
    status_code = client.dn_update(domain_name)
    if status_code != 200:
        logging.error(f"error updating {domain_name}")


@app.task
def daily_task():
    client_data = {
        "host": os.environ["API_HOST"],
        "username": os.environ["API_USERNAME"],
        "password": os.environ["API_PASSWORD"],
    }
    client = ApiClient(**client_data)
    client.login()
    dn_list = client.dn_list()
    for domain_name in dn_list:
        resolve.delay(client.model_dump_json(), domain_name)
    return "done"
