from datetime import datetime
from db import MainMeta
import ormar as orm
from .types import UserType

class User(orm.Model):

    id: int  = orm.Integer(primary_key=True)
    name: str = orm.String(max_length=100)
    username: str = orm.String(max_length=100, nullable=True, unique=True, index=True)
    email: str = orm.String(max_length=254, default = "", index= True)
    password: str = orm.Text(default = "")
    created_at: str = orm.DateTime(default = datetime.utcnow)
    type: UserType = orm.ForeignKey(
        UserType, nullable = False, ondelete='CASCADE', onupdate='CASCADE'
    )
    is_active: bool = orm.Boolean(default = True)
    privilege: int  = orm.Integer(default = 0)

    class Meta(MainMeta):
        tablename = "users"

    async def load_data(self):
        await self.type.load()
        return self
