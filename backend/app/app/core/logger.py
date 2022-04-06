import logging
import logging.config
from fastapi_helpers import get_logger_default_config
from .config import settings

logging.config.dictConfig(get_logger_default_config(settings))

logger = logging.getLogger("fastapi")