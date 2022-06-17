from utils import env_path
from fastapi_helpers import DefaultSettings
from typing import Optional


class Settings(DefaultSettings):
    app_name = "proyecto-redes"
    db_url: str = "sqlite:///database.db"
    port:Optional[str] = "80"
    version:str = "0.0.0.1"


settings = Settings(env_path)
