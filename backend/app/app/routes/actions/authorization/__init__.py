from fastapi import APIRouter
from . import login

router = APIRouter()

router.include_router(login.router, prefix="/login", tags=["login"])