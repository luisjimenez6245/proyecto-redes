from fastapi import APIRouter
from . import db_fill
router = APIRouter()

router.include_router(db_fill.router, tags=["db utils"])