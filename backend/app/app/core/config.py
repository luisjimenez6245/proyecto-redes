from utils import env_path
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name = "proyecto-redes"
    node_host:str = "0.0.0.0"
    port:Optional[str] = "80"
    db_url:str 
    debug:bool = True

settings = Settings(env_path)