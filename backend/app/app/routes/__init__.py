from flask import Blueprint
from .actions import action_blueprint
from .model import model_blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

api_blueprint.register_blueprint(action_blueprint)
api_blueprint.register_blueprint(model_blueprint)

blueprints = [api_blueprint]