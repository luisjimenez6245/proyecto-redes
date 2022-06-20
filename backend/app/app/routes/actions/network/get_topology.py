from operator import concat
from typing import Dict, List
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
    set_snmp
)
from core.controllers.scan_controller import (
    scan_by_interface,
)

from core.controllers.snmp import get_info

from models import Device, Interface

router = APIRouter()


async def get_old_topology() -> Dict[str, Device]:
    all_devices = await Device.objects.all()
    result = {}
    for device in all_devices:
        result[device.name] = device
    return result


async def save_interface_change(device: Device, interfaces: List[Dict]):
    old_interfaces = await Interface.objects.filter(
        device=device
    ).all()
    old_keys_interfaces = {}

    for interface in old_interfaces:
        old_keys_interfaces[interface.name] = interface

    new_interfaces = []
    no_changes_devices = []

    for interface in interfaces:
        name = interface['name']
        if name not in old_keys_interfaces:
            new_interfaces.append(interface)
        else:
            no_changes_devices.append(name)
    
    for key in old_keys_interfaces:
        if key not in no_changes_devices:
            await old_keys_interfaces[key].delete()
            print("Deleted interface: " + key)
    
    for interface in new_interfaces:
        name = interface['name']
        i = Interface(
            id=f"{device.name}-{name}",
            device=device,
            name=interface["name"],
            ip=interface["ip"],
            idnet=interface["idnet"],
        )
        await i.save()
        print("Added interface: " + i.id)


async def save_new_devices(devices: List[Dict], old_devices: Dict[str, Device]):
    no_changes_devices = []
    new_devices = []
    for device in devices:
        hostname = device["hostname"]
        if hostname not in old_devices:
            new_devices.append(device)
        else:
            await save_interface_change(old_devices[hostname], device["interfaces"])
            no_changes_devices.append(hostname)

    for key in old_devices:
        if key not in no_changes_devices:
            await old_devices[key].delete()
            print("Deleted device: " + key)

    for device in new_devices:
        ip = ""
        interfaces = device["interfaces"]
        data = {
            "location": "",
            "contact": "",
            "hostname": ""
        }
        if(len(interfaces)):
            ip = interfaces[0]["ip"]
            data = get_info(ip)
    
        d = Device(
            id=device["hostname"],
            ip = ip,
            name=device["hostname"],
            model="",
            contact= data["contact"],
            hostname=data["hostname"],
            location=data["location"],
        )
        await d.save()
        await save_interface_change(d, interfaces)
        print("Added device: " + d.id)


async def get_topology_from_db():
    body = scan_by_interface()
    old_devices = await get_old_topology()
    devices = body[0]
    await save_new_devices(devices, old_devices)
    return body


@router.post("/get_topology/")
async def get_topology():
    return await get_topology_from_db()


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
    protocols = ["eigrp", "ospf", "rip"]
    if(topology_type not in protocols):
        return "Invalid topology type"

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


@router.post("/set_snmp")
async def set_snmp_action(

):
    default_user = {
        "host": getGateway(),
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_ios",
        "secret": "cisco"
    }
    set_snmp(default_user)
    return "OK"
