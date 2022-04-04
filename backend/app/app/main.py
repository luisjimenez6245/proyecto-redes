from flask import Flask, request
from werkzeug.exceptions import HTTPException
from routes import blueprints
from db import database
from orjson import dumps
from core.logger import logger
from core.config import settings

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = settings.db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
database.init_app(app)
app.name = settings.app_name
app.config.from_object(settings)

for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.get("/")
def app_name():
    return {"app_name":settings.app_name}

@app.errorhandler(HTTPException)
def handle_exception(e: HTTPException):
    logger.error(e)
    response = e.get_response()
    response.data = dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
    app.run(host=settings.node_host,port=settings.port, debug=settings.debug)
