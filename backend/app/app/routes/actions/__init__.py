from flask import Blueprint
from . import health_check

action_blueprint  = Blueprint("actions", __name__, url_prefix="/actions")


action_blueprint.register_blueprint(health_check.router)