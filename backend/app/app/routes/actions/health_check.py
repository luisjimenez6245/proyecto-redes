from typing import Dict
from fastapi import APIRouter

router = APIRouter()

@router.get("/health-check")
def health_check() -> Dict[str, str]:
    return {"status": "healthy"}