from .model_router import DefaultModelRouter
from crud import session_crud
from models import Session

router = DefaultModelRouter(Session, session_crud).router
