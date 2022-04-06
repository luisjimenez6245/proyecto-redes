from typing import List
from models import User, Device
from models.relations import DeviceUser
from netmiko import ConnectHandler
from core.logger import logger

def connect_by_ssh(ip: str, commands: List[str], config: bool = False) -> List[str]:
    connection = ConnectHandler(
        ip=ip, device_type="cisco_ios", username='admin', password='admin')
    output = []
    if(not config):
        for command in commands:
            output.append(connection.send_command(command))
    else:
        for command in commands:
            output.append(connection.send_config_set(command))
    connection.disconnect()
    return output


def add_ssh_user(device: Device, user: User, device_user: DeviceUser) -> bool:
    ip = device.location.split(sep=",")[0]
    commands = [
        f"username {user.username} privilege {device_user.privilage} password {user.password}"
    ]
    try : 
        logs = connect_by_ssh(ip, commands, True)
        logger.info(logs)
        logs = connect_by_ssh(ip, ['wr'], False)
        logger.info(logs)
        return True
    except Exception as ex:
        logger.exception(ex)
        return False
    
def remove_ssh_user(device: Device, user: User) -> bool:
    ip = device.location.split(sep=",")[0]
    commands = [
        f"no username {user.username} password {user.password}"
    ]
    try : 
        logs = connect_by_ssh(ip, commands, True)
        logger.info(logs)
        logs = connect_by_ssh(ip, ['wr'], False)
        logger.info(logs)
        return True
    except Exception as ex:
        logger.exception(ex)
        return False

def update_ssh_user(device: Device, user : User, device_user: DeviceUser ) -> bool:
    if(remove_ssh_user(device, user)):
        return add_ssh_user(device, user, device_user)
    raise Exception("Error while updating ssh user")



