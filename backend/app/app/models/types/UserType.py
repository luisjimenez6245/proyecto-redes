from db import MainMeta
import ormar as orm
import uuid

class UserType(orm.Model):

    id: uuid.UUID = orm.UUID(primary_key=True, default=uuid.uuid4)
    name: str = orm.String(max_length=20, server_default='', unique=True)
    description: str = orm.String(max_length=50, server_default='')
    is_active: bool = orm.Boolean(default=False)

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "user_types"
