from  .. import oauth2_scheme
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from routes.utils.authorization import from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await from_token(token)
    if not user:
        print("sin llave")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
