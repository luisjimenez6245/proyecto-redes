from datetime import datetime
from db import MainMeta
import ormar as orm
from .User import User

class Session(orm.Model):
    id: int  = orm.Integer(primary_key=True)
    user:User = orm.ForeignKey(User, ondelete='CASCADE', onupdate='CASCADE')
    created_at: datetime = orm.DateTime(default=datetime.utcnow)
    valid_from: datetime = orm.DateTime(default=datetime.utcnow)
    valid_to: datetime = orm.DateTime(default=datetime.utcnow)
    token: str = orm.String(max_length=100, nullable=False)

    async def load_data(self):
        return self

    class Meta(MainMeta):
        tablename = "sessions"
