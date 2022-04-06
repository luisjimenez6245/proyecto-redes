from fastapi import APIRouter, Response, Form
from core.controllers import authorization
from pydantic import BaseModel
from orjson import dumps

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post('/')
async def login(
    *,
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


@router.post('/validate/{token}/')
async def validate_session(
    *,
    token: str,
    id: str = Form(...),
):
    result = await authorization.login_validate(token, id)
    return result


class LogoutRequest(BaseModel):
    token: str
    id: str = ""


@router.post("/logout/")
async def method_logout(
    *,
    request: LogoutRequest
):
    """
    Invalidate Session model to unauthorize an access to a computer
    """
    result = await authorization.logout(request.token)
    return result
