from typing import Dict, List
from netmiko import (ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException)
from core.logger import logger

class Router:
    destination_host: str
    management_ip: str


def show_dcp(ip: str) -> List[Router]:
    try:
        connnection = ConnectHandler(device_type='cisco_ios', ip=ip, username='cisco', password='cisco')
        return connnection.send_command('show cdp neighbors detail', use_textfsm=True)
    except NetmikoAuthenticationException as ex:
        logger.error('Authentication failed to device {}'.format(ip), exc_info=True)
        raise ex
    except NetmikoTimeoutException as ex:
        logger.error('Timeout to device {}'.format(ip), exc_info=True)
        raise ex
    except Exception as e:
        logger.error('Unknown error to device {}'.format(ip), exc_info=True)
        raise e

def get_fixed_ip(router: Router, principal_router: Router) -> str:
    helper = router.destination_host.partition(".")[0]
    result  = f"{helper}:{router.management_ip}"
    if helper == principal_router.destination_host:
            result  = f"{helper}:{principal_router.management_ip}"
    return result

def get_topology(root: Router) -> Dict[Router]:
    result = {}
    next_router = [root]
    visited_routers = []
    while next_router:
        current_router = next_router.pop()
        if current_router and current_router.management_ip is not None:
            parent_ip = get_fixed_ip(current_router, root)
            result[current_router.management_ip] = {}
            dcp_neighbors = show_dcp(current_router.management_ip)
            for item in dcp_neighbors:
                child_ip = get_fixed_ip(item, root)
                if child_ip not in visited_routers:
                    visited_routers.append(child_ip)
                    next_router.append(item)
                    result[parent_ip][child_ip] = {}
    return result

def reset_network():
    pass