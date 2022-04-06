from datetime import datetime
import ormar as orm
from db import MainMeta
from .User import User
from typing import List
from .relations import DeviceUser


class Device(orm.Model):

    id: int  = orm.Integer(primary_key=True)
    name: str = orm.String(max_length=100, nullable=False)
    model: str = orm.String(max_length=100, nullable=True)
    os: str = orm.String(max_length=20, nullable=False)
    location: str = orm.String(max_length=20, nullable=False)
    users: List = orm.ManyToMany(
        User, through=DeviceUser, ondelete='CASCADE', onupdate='CASCADE')
    created_at: datetime = orm.DateTime(default=datetime.utcnow)
    updated_at: datetime = orm.DateTime(default=datetime.utcnow)
    deleted_at: datetime = orm.DateTime(nullable=True)

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "devices"
