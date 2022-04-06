import ormar as orm
import uuid
from db import MainMeta
from .User import User
from datetime import datetime

class Report(orm.Model):

    id: uuid.UUID = orm.UUID(primary_key=True, default=uuid.uuid4)
    user: User = orm.ForeignKey(User, ondelete='CASCADE', onupdate='CASCADE')
    action: str = orm.String(max_length=100, nullable=False)
    created_date: datetime = orm.DateTime(default=datetime.utcnow)

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "reports"