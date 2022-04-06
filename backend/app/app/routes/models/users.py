from fastapi_helpers import DefaultModelRouter
from crud import user_crud
from models import User

router = DefaultModelRouter(User, user_crud).router
