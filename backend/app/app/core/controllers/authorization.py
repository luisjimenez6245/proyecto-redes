from typing import Optional
from orjson import dumps
from fastapi import Response
from crud import user_crud, session_crud
from models import User, Session
from secrets import token_urlsafe
from datetime import datetime, timedelta


def get_some_minutes_more():
    now = datetime.now()
    result = timedelta(minutes=45) + now
    return result


async def get_user(username: str, password: str) -> Optional[User]:
    user = await user_crud.get_by_username(username)
    if user and user.password == password:
        return user
    return None


async def login(username: str, password: str):
    user = await get_user(username, password)
    if user:
        session = Session(
            user=user,
            token=token_urlsafe(32),
            valid_from=datetime.utcnow(),
            valid_to=datetime.utcnow() + timedelta(days=1),
        )
        session = await session_crud.create(session)
        await session.user.load()
        await session.user.type.load()
        return session
    return None


async def login_validate(token, id):
    session = await Session.objects.get_or_none(token=token, )
    if(session is not None):
        await session.update(
            valid_to=get_some_minutes_more()
        )
        return session
    return Response(
            dumps({'status': 'error'}),
            status_code=403,
            media_type='application/json'
        )


async def logout(token):
    session = await Session.objects.get_or_none(token=token, )
    if(session is not None):
        await session.update(
            user=session.user.id,
            valid_to=datetime.now()
        )
        return Response(
            dumps({'status': 'ok'}),
            status_code=200,
            media_type='application/json'
        )
    return Response(
            dumps({'status': 'error'}),
            status_code=400,
            media_type='application/json'
        )
