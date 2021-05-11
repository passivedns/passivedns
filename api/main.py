import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from controllers.alert import alert_blueprint
from controllers.auth import auth_blueprint
from controllers.channels import channels_blueprint
from controllers.channels_admin import channels_admin_blueprint
from controllers.domain_name import domain_name_blueprint
from controllers.infos import infos_blueprint
from controllers.resolution import resolution_blueprint
from controllers.scheduler import scheduler_blueprint
from controllers.scheduler_admin import scheduler_admin_blueprint
from controllers.tag import tag_blueprint
from controllers.tag_dn_ip import tag_dn_ip_blueprint
from controllers.user_channel import users_channel_blueprint
from controllers.users import users_blueprint
from controllers.users_admin import users_admin_blueprint

app = Flask("Passive DNS API")
CORS(app)

app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)


app.register_blueprint(auth_blueprint)
app.register_blueprint(users_blueprint)
app.register_blueprint(users_admin_blueprint)
app.register_blueprint(domain_name_blueprint)
app.register_blueprint(resolution_blueprint)
app.register_blueprint(scheduler_blueprint)
app.register_blueprint(scheduler_admin_blueprint)
app.register_blueprint(channels_blueprint)
app.register_blueprint(channels_admin_blueprint)
app.register_blueprint(users_channel_blueprint)
app.register_blueprint(tag_blueprint)
app.register_blueprint(tag_dn_ip_blueprint)
app.register_blueprint(alert_blueprint)

app.register_blueprint(infos_blueprint)


debug = os.environ['DEBUG'] == "1"

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug)
