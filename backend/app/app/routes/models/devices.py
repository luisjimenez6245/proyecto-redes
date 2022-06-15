from .model_router import DefaultModelRouter
from crud import device_crud
from models import Device

router = DefaultModelRouter(Device, device_crud).router
