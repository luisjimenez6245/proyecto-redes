from fastapi_helpers import DefaultModelRouter
from crud.types import user_type_crud
from models.types import UserType

router = DefaultModelRouter(UserType, user_type_crud).router
