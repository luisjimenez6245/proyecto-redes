import ormar as orm
from db import MainMeta
from .User import User
from datetime import datetime

class Report(orm.Model):

    id: int  = orm.Integer(primary_key=True)
    action: str = orm.String(max_length=100, nullable=False)
    created_date: datetime = orm.DateTime(default=datetime.utcnow)

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "reports"