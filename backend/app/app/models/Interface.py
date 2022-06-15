import ormar as orm
from db import MainMeta
from .Device import Device
from ormar import post_save, post_update, pre_delete
from .Report import Report
from datetime import datetime

class Interface(orm.Model):

    id: str  = orm.String(max_length=40,primary_key=True)
    device: Device = orm.ForeignKey(Device, ondelete='CASCADE', onupdate='CASCADE')
    name: str = orm.String(max_length=100, nullable=False)
    ip: str = orm.String(max_length=20, nullable=False)
    idnet: str = orm.String(max_length=20, nullable=False)

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "interfaces"



@post_save(Interface)
async def post_update_interface(
    sender,
    instance: Interface,
    **kwargs
):
    r = Report(
        action=f"Interface created {instance.name}",
        created_date=datetime.utcnow(),
    )
    await Report.save(r)
    from core.controllers.email_controller import send_email
    send_email(r.action)


@post_update(Interface)
async def post_update_interface(
    sender,
    instance: Interface,
    **kwargs
):
    r = Report(
        action=f"Interface updated {instance.name}",
        created_date=datetime.utcnow(),
    )
    await Report.save(r)
    from core.controllers.email_controller import send_email
    send_email(r.action)


@pre_delete(Interface)
async def post_save_interface(
    sender,
    instance: Interface,
    **kwargs
):
    r = Report(
        action=f"Interface deleted {instance.name}",
        created_date=datetime.utcnow(),
    )
    await Report.save(r)
    from core.controllers.email_controller import send_email
    send_email(r.action)