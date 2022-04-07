from asyncio.log import logger
from typing import Optional, Union, Dict
from fastapi_helpers import to_dict
from fastapi_helpers import BaseCrud
from models import User
from models.types import UserType

class UserCrud(BaseCrud):

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.model.objects.get_or_none(username=username)
        if result:
            return result
        result = await self.model.objects.get_or_none(email=username)
        return result

    async def create(self, model_in: Optional[Union[Dict, User]]) -> Optional[User]:
        model_in = to_dict(model_in)
        user_type_name = model_in.pop('type', None)
        if isinstance(user_type_name,str):
            user_type = await UserType.objects.get_or_create(name=user_type_name)
            model_in['type'] = user_type
        elif isinstance(user_type_name, dict):
            user_type = await UserType.objects.get_or_create(name=model_in["name"], description = model_in["description"])
            model_in['type'] = user_type
        user =  await super().create(model_in)
        if user_type.name == 'admin':
            pass
        # carga usuarios ssh
        return user

crud = UserCrud(User)
