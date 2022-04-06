from fastapi import APIRouter

from . import utils
from . import health_check
from . import authorization
from . import network

router = APIRouter()

router.include_router(utils.router)
router.include_router(health_check.router)
router.include_router(authorization.router)
router.include_router(network.router)