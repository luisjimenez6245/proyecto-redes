from fastapi import APIRouter, Depends, Response
from ..injections.authorization_inyection import get_current_user
from core.controllers.network_controller import createUserRouter, deleteUserRouter, getGateway
from core.controllers.remote_connection import sshAllRouters
from orjson import dumps
from models import User


router = APIRouter()


@router.post("/enable-ssh")
async def enable_ssh():
    user_to_ssh = {
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
        "device_type": "cisco_ios_telnet",
        "host": getGateway()
    }
    try:
        sshAllRouters(user_to_ssh)
        return Response(status_code=200, content=dumps({"message": "SSH enabled"}))
    except Exception as e:
        return Response(status_code=500, content=dumps({"message": str(e)}))



@router.post("/create-ssh-user")
async def create_ssh_user(
    *,
    changed_user_id: str,
    privilege: int,
    principal_user: User = Depends(get_current_user),
):
    if(principal_user.type.name == "admin"):
        changed_user = await User.objects.get_or_none(id=changed_user_id)
        if(changed_user is not None):
            user_to_ssh = {
                "username": changed_user.username,
                "password": changed_user.password,
                "privilege": privilege,
            }
            createUserRouter(
                {"username": "cisco", "password": "cisco",
                    "host": getGateway(), "device_type": "cisco_ios"},
                user_to_ssh
            )
            changed_user.privilege = privilege
            await changed_user.update(["privilege"])
            return Response(dumps({"message": "User created"}), status_code=200)
    return Response(
        dumps({"message": "You are not authorized to perform this action"}),
        status_code=403
    )


@router.post("/delete-ssh-user")
async def delete_ssh_user(
    *,
    changed_user_id: str,
    principal_user: User = Depends(get_current_user),
):
    if(principal_user.type.name == "admin"):
        changed_user = await User.objects.get_or_none(id=changed_user_id)
        if(changed_user is not None):
            user_to_ssh = {
                "username": changed_user.username,
                "password": changed_user.password,
                "privilege": changed_user.privilege,
            }
            deleteUserRouter(
                {"username": "cisco", "password": "cisco",
                    "host": getGateway(), "device_type": "cisco_ios"},
                user_to_ssh
            )
            return Response(dumps({"message": "User deleted"}), status_code=200)
    return Response(
        dumps({"message": "You are not authorized to perform this action"}),
        status_code=403
    )


@router.post("/change-ssh-user-privilege")
async def change_ssh_user_privilege(
    *,
    changed_user_id: str,
    privilege: int,
    principal_user: User = Depends(get_current_user),
):
    if(principal_user.type.name == "admin"):
        changed_user = await User.objects.get_or_none(id=changed_user_id)
        if(changed_user is not None):
            user_to_ssh = {
                "username": changed_user.username,
                "password": changed_user.password,
                "privilege": changed_user.privilege,
            }
            deleteUserRouter(
                {"username": "cisco", "password": "cisco",
                    "host": getGateway(), "device_type": "cisco_ios"},
                user_to_ssh
            )
            user_to_ssh["privilege"] = privilege
            createUserRouter(
                {"username": "cisco", "password": "cisco",
                    "host": getGateway(), "device_type": "cisco_ios"},
                user_to_ssh
            )
            changed_user.privilege = privilege
            await changed_user.update(["privilege"])
            return Response(dumps({"message": "User updated"}), status_code=200)
    return Response(
        dumps({"message": "You are not authorized to perform this action"}),
        status_code=403
    )
