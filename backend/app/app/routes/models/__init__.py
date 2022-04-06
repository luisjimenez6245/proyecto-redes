from fastapi import APIRouter
from . import users
from . import reports
from . import packages
from . import interfaces
from . import devices
from . import sessions

router_models = APIRouter()

router_models.include_router(users.router, prefix="/users", tags=["users"])
router_models.include_router(reports.router, prefix="/reports", tags=["reports"])
router_models.include_router(packages.router, prefix="/packages", tags=["packages"])
router_models.include_router(interfaces.router, prefix="/interfaces", tags=["interfaces"])
router_models.include_router(devices.router, prefix="/devices", tags=["devices"])
router_models.include_router(sessions.router, prefix="/sessions", tags=["sessions"])