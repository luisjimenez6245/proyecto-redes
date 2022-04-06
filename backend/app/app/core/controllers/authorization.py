from crud import user_crud

async def login(username: str, password: str):
    user = await user_crud.get_by_username(username)
    if user and user.password == password:
        return user
    return None