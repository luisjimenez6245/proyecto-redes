from flask import Blueprint
from . import users

model_blueprint  = Blueprint("models", __name__, url_prefix="/models")

model_blueprint.register_blueprint(users.router)