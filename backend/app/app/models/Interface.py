import ormar as orm
import uuid
from db import MainMeta
from .Device import Device

class Interface(orm.Model):

    id: uuid.UUID = orm.UUID(primary_key=True, default=uuid.uuid4)
    device: Device = orm.ForeignKey(Device, ondelete='CASCADE', onupdate='CASCADE')
    name: str = orm.String(max_length=100, nullable=False)
    ip: str = orm.String(max_length=20, nullable=False)
    mac: str = orm.String(max_length=20, nullable=False)
    mask: str = orm.String(max_length=20, nullable=False)

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "interfaces"