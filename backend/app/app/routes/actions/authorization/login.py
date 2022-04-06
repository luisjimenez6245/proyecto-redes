from fastapi import APIRouter, Response
from core.controllers import authorization
from pydantic import BaseModel
from orjson import dumps

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post('/')
async def login(
    request: LoginRequest
):
    session = await authorization.login(request.username, request.password)
    if session:
        return session
    return Response(
        dumps({
            'detail': 'Invalid credentials'
        }), 403, 
        media_type='application/json'
    )
