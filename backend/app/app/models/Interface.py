import ormar as orm
import uuid
from db import MainMeta

class Interface(orm.Model):

    id: uuid.UUID = orm.UUID(primary_key=True, default=uuid.uuid4)


    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "interfaces"