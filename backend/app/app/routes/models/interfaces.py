from .model_router import DefaultModelRouter
from crud import interface_crud
from models import Interface

router = DefaultModelRouter(Interface, interface_crud).router
