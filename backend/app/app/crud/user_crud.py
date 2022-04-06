from typing import Optional
from fastapi_helpers import BaseCrud
from models import User

class UserCrud(BaseCrud):

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.model.objects.get_or_none(username=username)
        if result:
            return result
        result = await self.model.objects.get_or_none(email=username)
        return result

crud = UserCrud(User)