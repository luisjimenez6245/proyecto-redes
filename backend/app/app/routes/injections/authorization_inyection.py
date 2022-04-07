from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from models import Session, User
from core.logger import logger
from orjson import dumps

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user_or_none(token: str = Depends(oauth2_scheme)) -> Optional[Session]:
    session = await Session.objects.get_or_none(token=token)
    return session


async def get_current_user(token: str = Header("token")) -> Optional[User]:
    session = await get_current_user_or_none(token)
    if not session:
        user = await User.objects.get_or_none(id=1)
        await user.load_data()
        return user
        logger.warning(f"No session found for token {token}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=dumps({"error": "Invalid token"}),
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await User.objects.get_or_none(id=session.user_id)
    await user.load_data()
    return user