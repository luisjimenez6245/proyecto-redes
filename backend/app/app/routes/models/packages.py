from fastapi_helpers import DefaultModelRouter
from crud import package_crud
from models import Package

router = DefaultModelRouter(Package, package_crud).router
