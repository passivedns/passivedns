from flask import Blueprint, request
from flask_jwt_extended import create_access_token, decode_token, get_jwt, jwt_required

from db.database import ObjectNotFound
from models.user import User
from views.misc import error_view, valid_view
from views.token import token_view

auth_blueprint = Blueprint("auth", __name__)


def post():
    try:
        body = request.get_json()
        identity = body.get('identity')
        password = body.get('password')

        if identity is None or identity == '' or password is None or password == '':
            return error_view(400, 'missing parameter')

        if User.exists_from_email(identity):
            # assume identity is email
            user = User.get_from_email(identity)
        else:
            # assume identity is username
            user = User.get(identity)

        if not user.verify_password(password):
            return error_view(401, "error logging in")

        # creating JWT
        # https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
        additional_claims = dict(role=user.role)
        access_token = create_access_token(identity=user.username, additional_claims=additional_claims)

        return token_view(access_token)

    except ObjectNotFound:
        return error_view(404, "error logging in")


@auth_blueprint.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        return post()


@auth_blueprint.route("/login", methods=['GET'])
@jwt_required()
def check_jwt():
    if request.method == 'GET':
        try:
            token = get_jwt()
            return valid_view("token is valid")
        except Exception:
            return error_view(400, "invalid token")


