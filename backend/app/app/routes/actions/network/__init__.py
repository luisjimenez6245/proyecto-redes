from fastapi import APIRouter
from .  import get_topology

router = APIRouter(prefix="/network")

router.include_router(get_topology.router, tags=["network"])
