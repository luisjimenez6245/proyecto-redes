import subprocess
from fastapi import APIRouter
from core.controllers.snmp import SNMP, get_info
from core.controllers.network_controller import update_router_snmp
from pydantic import BaseModel

router = APIRouter(prefix="/snmp")

@router.get("/")
async def root():
    obj = SNMP()
    data = obj.getInterfacesCounters("10.0.1.254", "1/1", "10.0.1.253", "1/1")
    return data[1]


@router.get("/info/{ip}")
async def info(
    ip: str
):
    return get_info(ip)


class DataIn(BaseModel):
    id: str
    type: str
    value: str


@router.post("/update/")
async def update(
    *,
    data: DataIn,
):
    await update_router_snmp(data.id, data.type, data.value)
    return {"status": "ok"}
