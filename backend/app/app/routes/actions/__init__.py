from fastapi import APIRouter

from . import utils
from . import health_check

router = APIRouter()

router.include_router(utils.router)
router.include_router(health_check.router)