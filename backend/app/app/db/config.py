from fastapi_helpers import DbConfig
from core.config import settings
from core.logger import logger
db_config = DbConfig(settings, logger)
