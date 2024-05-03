import os

from flask import Blueprint

from utils import config
from views.infos import infos_view

infos_blueprint = Blueprint("infos", __name__)


@infos_blueprint.route("/infos", methods=['GET'])
def get_infos():
    return infos_view(
        config.g.VERSION,
        config.g.JOB_URL,
        config.g.COMMIT_SHA,
    )
