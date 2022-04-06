from typing import Optional
from crud import user_crud, session_crud
from models import User, Session
from secrets import token_urlsafe
from datetime import datetime, timedelta

async def get_user(username: str, password: str) -> Optional[User]:
    user = await user_crud.get_by_username(username)
    if user and user.password == password:
        return user
    return None


async def login(username: str, password: str):
    user = await get_user(username, password)
    if user:
        session = Session(
            user = user, 
            token = token_urlsafe(32), 
            valid_from = datetime.utcnow(), 
            valid_to = datetime.utcnow() + timedelta(days=1),
        )
        session = await session_crud.create(session)
        return session
    return None