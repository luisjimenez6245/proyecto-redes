from typing import Dict, List
from models.Device import Device
import netifaces
from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException
)
from .remote_connection import commandAllRouters, telnetConexion, sshConexion, upSSh, neighborsSSH
try:
    from core.logger import logger
except:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)


class Router:
    destination_host: str
    management_ip: str

    def __str__(self) -> str:
        return f"{self.destination_host} ({self.management_ip})"


def snmp_commands_create():
    cmd = [
        "conf t",
        "snmp-server view v3Read iso included",
        "snmp-server view v3Write iso include",
        "snmp-server group REDES v3 auth read v3Read write v3Write",
        "snmp-server contact elferpro@gmail.com",
        "snmp-server location salonredes",
        f"snmp-server user admin REDES v3 auth sha administrador_snmp priv des56 administrador_snmp",
        "end"]
    return cmd


def snmp_commands_update_location(location):
    cmd = [
        "conf t",
        "snmp-server view v3Read iso included",
        "snmp-server view v3Write iso include",
        f"snmp-server location {location}",
        "end"]
    return cmd


def snmp_commands_update_contact(contact):
    cmd = [
        "conf t",
        "snmp-server view v3Read iso included",
        "snmp-server view v3Write iso include",
        f"snmp-server contact {contact}",
        "end"]
    return cmd
    

def snmp_commands_update_hostname(hostname):
    cmd = [
        "conf t",
        f"hostname {hostname}",
        "end"]
    return cmd

async def update_router_snmp(router_id, type, value):
    router = await Device.objects.get(id=router_id)
    cmd = []
    if(type == 'location'):
        cmd = snmp_commands_update_location(value)
        router.location = value
    elif(type == 'contact'):
        cmd = snmp_commands_update_contact(value)
        router.contact = value
    elif(type == 'hostname'):
        cmd = snmp_commands_update_hostname(value)
        router.hostname = value

    await router.update()
    sshConexion({
        "host": getGateway(),
        "username": "cisco",
        "password": "cisco",
        "device_type": "cisco_ios",
        "secret": "cisco",
        "ip": router.ip,
    }, cmd)


def show_dcp(ip: str,  child_ips: List[Router] = None) -> List[Router]:
    try:
        connnection = ConnectHandler(
            device_type='cisco_ios', ip=ip, username='cisco', password='cisco')
        should_parse_output = True
        if child_ips:
            for child in child_ips:
                if child.management_ip == ip:
                    continue
                else:
                    should_parse_output = True
                    logger.info(
                        "connecting to child router {} {}".format(child, ""))
                    res = connnection.send_command_timing(
                        f"telnet {child.management_ip}")
                    res = connnection.send_command_timing("cisco\n")
                    res = connnection.send_command_timing("cisco\n")
                    logger.info(
                        "connected to child router {} {}".format(child, res))

        neigs = connnection.send_command_timing(
            'show cdp neighbors detail', use_textfsm=should_parse_output)
        result = []
        if child_ips:
            for child in child_ips:
                if child.management_ip == ip:
                    continue
                connnection.send_command_timing(f"exit")
        logger.info(f"neigs: {neigs}")
        for neig in neigs:
            r = Router()
            r.__dict__.update(neig)
            result.append(r)
        return result
    except NetmikoAuthenticationException as ex:
        logger.error(
            'Authentication failed to device {}'.format(ip), exc_info=True)
        raise ex
    except NetmikoTimeoutException as ex:
        logger.error('Timeout to device {}'.format(ip), exc_info=True)
        raise ex
    except Exception as e:
        logger.error('Unknown error to device {}'.format(ip), exc_info=True)
        raise e


def get_fixed_ip(router: Router, principal_router: Router) -> str:
    helper = router.destination_host.partition(".")[0]
    result = f"{helper}:{router.management_ip}"
    if helper == principal_router.destination_host:
        result = f"{helper}:{principal_router.management_ip}"
    return result


def get_topology(root: Router) -> Dict:
    result = {}
    next_router = [root]
    router_info = []
    visited_routers = [root.destination_host]
    root_key = get_fixed_ip(root, root)
    result[root_key] = {}
    while next_router:
        current_router = next_router.pop()
        logger.info(f"current router {current_router}")
        if current_router and current_router.management_ip is not None:
            parent_ip = get_fixed_ip(current_router, root)
            result_helper = {
                parent_ip: {},
            }
            dcp_neighbors = show_dcp(root.management_ip, [current_router])
            for item in dcp_neighbors:
                child_ip = get_fixed_ip(item, root)
                if item.destination_host not in visited_routers:
                    visited_routers.append(item.destination_host)
                    next_router.append(item)
                    router_info.append(item)
                    result_helper[parent_ip][child_ip] = {}
            result = {
                **result,
                **result_helper
            }
    for item in router_info:
        print(item.__dict__)
    return result


def reset_network():
    pass


if __name__ == "__main__":
    main_router = Router()
    main_router.destination_host = "R3"
    main_router.management_ip = "10.0.7.254"
    logger.info(get_topology(main_router))


def getIpDirectlyConnected(user):
    output = sshConexion(user, ["ssh -l "+user.get("username") +
                         user.get("host"), user.get("password"), "show ip route"])
    response = output["show ip route"]
    listResponse = response.split('\n')
    listIP = []
    findString = ""
    for response in listResponse:
        findString = response
        res = findString.find("is directly connected")
        if(res > -1):
            listIP.append(findString[:res].replace("C", "").replace(" ", ""))
    return listIP


def comandsRip(list):
    commandsRip = ["conf terminal", "router rip", "version 2"]
    listIp = []
    listIp = list
    for ip in listIp:
        commandsRip.append("network "+ip)
    commandsRip.append("no auto-summary")
    commandsRip.append("exit")
    # sshConexion(user,commandsRip)
    return commandsRip


def comandsIgrp(list):
    commandsRip = ["conf terminal", "router eigrp 1"]
    listIp = []
    listIp = list
    for ip in listIp:
        commandsRip.append("network "+ip)
    commandsRip.append("exit")
    # sshConexion(user,commandsRip)
    return commandsRip


def comandsOSPF(list):
    commandsOspf = ["conf terminal", "router ospf 1"]
    listIp = []
    listIp = list
    for ip in listIp:
        commandsOspf.append("network "+ip+" 0.0.0.255 "+" area 0")
    commandsOspf.append("exit")
    # sshConexion(user,commandsRip)
    return commandsOspf


def upRip(user):

    listIp = getIpDirectlyConnected(user)
    commandsRip = comandsRip(listIp)
    print(commandsRip)
    sshConexion(user, commandsRip)
    respuestaNeighbors = neighborsSSH(user)

    for router in respuestaNeighbors:

        respuestaSsh = sshConexion(user, ["show cdp entry "+router])
        respuestaCdp = respuestaSsh["show cdp entry "+router]
        # [3] da el Id del router, [8] da la ip de la interfaz del router
        respuestaCdp = respuestaCdp.split()
        print("Respuesta de " + router)
        commandsSend = [
            "ssh -l "+user.get("username")+" " + respuestaCdp[8], user.get("password")]
        commandsSend.extend(["show ip route"])
        output = sshConexion(user, commandsSend)

        response = output["show ip route"]
        listResponse = response.split('\n')
        listIP = []
        findString = ""
        for response in listResponse:
            findString = response
            res = findString.find("is directly connected")
            if(res > -1):
                listIP.append(findString[:res].replace(
                    "C", "").replace(" ", ""))

        print(comandsRip(listIP))
        commandsSend = [
            "ssh -l "+user.get("username")+" " + respuestaCdp[8], user.get("password")]
        newComandsRip = comandsRip(listIP)
        newComandsRip.extend(["end"])
        newComandsRip.extend(["exit"])
        commandsSend.extend(newComandsRip)
        sshConexion(user, commandsSend)

        # print(respuestaCdp)


def upEigrp(user):

    listIp = getIpDirectlyConnected(user)
    commandsRip = comandsIgrp(listIp)
    print(commandsRip)
    sshConexion(user, commandsRip)
    respuestaNeighbors = neighborsSSH(user)

    for router in respuestaNeighbors:

        respuestaSsh = sshConexion(user, ["show cdp entry "+router])
        respuestaCdp = respuestaSsh["show cdp entry "+router]
        # [3] da el Id del router, [8] da la ip de la interfaz del router
        respuestaCdp = respuestaCdp.split()
        print("Respuesta de " + router)
        commandsSend = [
            "ssh -l "+user.get("username")+" " + respuestaCdp[8], user.get("password")]
        commandsSend.extend(["show ip route"])
        output = sshConexion(user, commandsSend)

        response = output["show ip route"]
        listResponse = response.split('\n')
        listIP = []
        findString = ""
        for response in listResponse:
            findString = response
            res = findString.find("is directly connected")
            if(res > -1):
                listIP.append(findString[:res].replace(
                    "C", "").replace(" ", ""))

        commandsSend = [
            "ssh -l "+user.get("username")+" " + respuestaCdp[8], user.get("password")]
        newComandsIgrp = comandsIgrp(listIP)
        newComandsIgrp.extend(["end"])
        newComandsIgrp.extend(["exit"])
        print(newComandsIgrp)
        commandsSend.extend(newComandsIgrp)
        sshConexion(user, commandsSend)


def create_wildcard(net):
    wildcard = []
    for i in range(4):
        wildcard.append(net[i]-255)
        if wildcard[i] < 0:
            wildcard[i] = -wildcard[i]
    return wildcard


def createUserRouter(device, user):
    # device es la cuenta activa de ssh y user es la lista con los datos del usuario a agregar
    commandAllRouters(device, ["enable", "configure terminal", "username "+user["username"] +
                      " privilege " + str(user["privilege"]) + " password "+user["password"], "end"])


def deleteUserRouter(device, user):
    commandAllRouters(device, ["enable", "configure terminal", "No username "+user["username"] +
                      " privilege " + str(user["privilege"]) + " password "+user["password"], "end"])


def downRip(user):
    commandAllRouters(user, ["conf terminal", "no router rip", "end"])


def downEigrp(user):
    commandAllRouters(user, ["conf terminal", "no router eigrp 1", "end"])


def upOspf(user):
    listIp = getIpDirectlyConnected(user)
    commandsOspf = comandsOSPF(listIp)
    print(commandsOspf)
    sshConexion(user, commandsOspf)
    respuestaNeighbors = neighborsSSH(user)

    for router in respuestaNeighbors:

        respuestaSsh = sshConexion(user, ["show cdp entry "+router])
        respuestaCdp = respuestaSsh["show cdp entry "+router]
        # [3] da el Id del router, [8] da la ip de la interfaz del router
        respuestaCdp = respuestaCdp.split()
        print("Respuesta de " + router)
        commandsSend = [
            "ssh -l "+user.get("username")+" " + respuestaCdp[8], user.get("password")]
        commandsSend.extend(["show ip route"])
        output = sshConexion(user, commandsSend)

        response = output["show ip route"]
        listResponse = response.split('\n')
        listIP = []
        findString = ""
        for response in listResponse:
            findString = response
            res = findString.find("is directly connected")
            if(res > -1):
                listIP.append(findString[:res].replace(
                    "C", "").replace(" ", ""))

        commandsSend = [
            "ssh -l "+user.get("username")+" " + respuestaCdp[8], user.get("password")]
        newComandsOspf = comandsOSPF(listIP)
        newComandsOspf.extend(["end"])
        newComandsOspf.extend(["exit"])
        print(newComandsOspf)
        commandsSend.extend(newComandsOspf)
        sshConexion(user, commandsSend)


def downOspf(user):
    commandAllRouters(user, ["conf terminal", "no router ospf 1"])


def set_snmp(user):
    commandAllRouters(user, snmp_commands_create())


def getGateway():
    gws = netifaces.gateways()
    gateway = gws['default'][netifaces.AF_INET][0]
    return gateway
