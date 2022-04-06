from fastapi import APIRouter
from . import user_types

router_model_types = APIRouter()

router_model_types.include_router(user_types.router, prefix="/user_types", tags=["user_types"])