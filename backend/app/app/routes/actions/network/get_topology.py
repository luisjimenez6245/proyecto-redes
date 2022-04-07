from fastapi import APIRouter
from core.controllers.network_controller import (
    neighborsSSH,
    getGateway,
    upEigrp,
    upOspf,
    upRip,
    downEigrp,
    downOspf,
    downRip,
)

router = APIRouter()


@router.get("/get_topology")
async def get_topology():
    return neighborsSSH({
        "host": getGateway(),
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_ios",
        "secret": "cisco"
    })


@router.post("/set_topology")
async def set_topology(
    *,
    topology_type: str,
):
    default_user = {
        "host": getGateway(),
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_ios",
        "secret": "cisco"
    }
    downOspf(default_user)
    downEigrp(default_user)
    downRip(default_user)
    if topology_type == "eigrp":
        return upEigrp(default_user)
    elif topology_type == "ospf":
        return upOspf(default_user)
    elif topology_type == "rip":
        return upRip(default_user)
    else:
        return "Invalid topology type"
