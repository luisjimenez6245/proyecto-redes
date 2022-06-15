from datetime import datetime
import ormar as orm
from db import MainMeta
from .User import User
from typing import List
from .relations import DeviceUser
from ormar import post_save, post_update, pre_delete
from .Report import Report


class Device(orm.Model):

    id: str = orm.String(primary_key=True, max_length=20)

    ip:str = orm.String(max_length=20, nullable=True)


    name: str = orm.String(max_length=100, nullable=False)
    model: str = orm.String(max_length=100, nullable=True)

    location: str = orm.String(max_length=100, nullable=True)
    contact: str = orm.String(max_length=100, nullable=True)
    hostname: str = orm.String(max_length=100, nullable=True)

    users: List = orm.ManyToMany(
        User, through=DeviceUser, ondelete='CASCADE', onupdate='CASCADE')
    created_at: datetime = orm.DateTime(default=datetime.utcnow)
    updated_at: datetime = orm.DateTime(default=datetime.utcnow)
    deleted_at: datetime = orm.DateTime(nullable=True)

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "devices"


@post_save(Device)
async def post_update_device(
    sender,
    instance: Device,
    **kwargs
):
    r = Report(
        action=f"Device created {instance.name}",
        created_date=datetime.utcnow(),
    )
    await Report.save(r)
    from core.controllers.email_controller import send_email
    send_email(r.action)


@post_update(Device)
async def post_update_device(
    sender,
    instance: Device,
    **kwargs
):
    r = Report(
        action=f"Device updated {instance.name}",
        created_date=datetime.utcnow(),
    )
    await Report.save(r)
    from core.controllers.email_controller import send_email
    send_email(r.action)


@pre_delete(Device)
async def post_save_device(
    sender,
    instance: Device,
    **kwargs
):
    r = Report(
        action=f"Device deleted {instance.name}",
        created_date=datetime.utcnow(),
    )
    await Report.save(r)
    from core.controllers.email_controller import send_email
    send_email(r.action)
