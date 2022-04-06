import ormar as orm
from db import MainMeta
from datetime import datetime

class Package(orm.Model):

    id: int  = orm.Integer(primary_key=True)
    created_at: datetime = orm.DateTime(default=datetime.utcnow)
    from_ip = orm.String(max_length=20, nullable=False, index = True)
    to_ip = orm.String(max_length=20, nullable=False, index = True)
    content: str = orm.Text(nullable=False, default = "")

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "packages"