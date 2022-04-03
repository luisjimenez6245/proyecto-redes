from flask import Flask, request
from werkzeug.exceptions import HTTPException
from core.config import settings
from routes import blueprints
from core.logger import logger
from orjson import dumps

app = Flask(__name__)
app.name = settings.app_name
app.config.from_object(settings)

for blueprint in blueprints:
    app.register_blueprint(blueprint)


@app.get("/")
def app_name():
    return {"app_name":settings.app_name}

@app.errorhandler(HTTPException)
def handle_exception(e):
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
