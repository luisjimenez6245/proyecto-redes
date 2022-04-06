from datetime import datetime
from db import MainMeta
import ormar as orm
import uuid
from .User import User

class Session(orm.Model):
    id: uuid.UUID = orm.UUID(primary_key=True, default=uuid.uuid4)
    user:User = orm.ForeignKey(User, ondelete='CASCADE', onupdate='CASCADE')
    created_at: datetime = orm.DateTime(default=datetime.utcnow)
    valid_from: datetime = orm.DateTime(default=datetime.utcnow)
    valid_to: datetime = orm.DateTime(default=datetime.utcnow)
    token: str = orm.String(max_length=100, nullable=False)

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "sessions"
