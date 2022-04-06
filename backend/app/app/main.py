import logging.config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_helpers import get_logger_default_config
from core.config import settings
from core.logger import logger
from db.config import db_config
from routes import routers
from fastapi_helpers import HeadersMiddleware

logging.config.dictConfig(get_logger_default_config(settings))

app = FastAPI(
    title= settings.app_name,
    version=settings.version,
    on_startup=[db_config.connect_db],
    on_shutdown=[db_config.disconnect_db],
    openapi_url=settings.get_open_api_path(),   
)

app.add_middleware(
    HeadersMiddleware,
    headers={
        "Access-Control-Allow-Headers": "Authorization, Content-Type, X-Gitlab-Token, X-Gitlab-Event",
    },
    logger=logger,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "Access-Control-Allow-Headers",
        "X-Process-Time",
    ]
)

for route in routers:
    app.include_router(route)


@app.get("/")
async def root():
    v = app.title
    return {"app": v, "version": settings.version}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=settings.is_development(),
        port=int(settings.port),
        workers=4
    )
