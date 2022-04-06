from email.policy import default
import ormar as orm
import uuid
from db import MainMeta

class DeviceUser(orm.Model):

    id: str = orm.String(primary_key=True, default=uuid.uuid4, max_length=36)
    privilage: int = orm.Integer(nullable=False, default = 0)


    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "device_users"