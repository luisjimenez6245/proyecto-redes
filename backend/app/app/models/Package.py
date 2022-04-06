import ormar as orm
import uuid
from db import MainMeta
from datetime import datetime

class Package(orm.Model):

    id: uuid.UUID = orm.UUID(primary_key=True, default=uuid.uuid4)
    created_at: datetime = orm.DateTime(default=datetime.utcnow)
    from_ip = orm.String(max_length=20, nullable=False, index = True)
    to_ip = orm.String(max_length=20, nullable=False, index = True)
    content: str = orm.Text(nullable=False, default = "")

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "packages"