import os

from flask import Blueprint

from views.infos import infos_view

infos_blueprint = Blueprint("infos", __name__)


@infos_blueprint.route("/infos", methods=['GET'])
def get_infos():
    return infos_view(
        os.environ['VERSION'],
        os.environ['JOB_URL'],
        os.environ['COMMIT_SHA'],
    )
