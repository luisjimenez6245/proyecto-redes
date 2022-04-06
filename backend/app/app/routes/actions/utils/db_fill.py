from fastapi import Request, APIRouter
from db.seeder import db_fill
from core.config import settings
router = APIRouter()

if settings.is_development():
    @router.get("/db_fill/")
    async def get_all(request: Request = {}):
        r = await db_fill()
        return {"status": r}

