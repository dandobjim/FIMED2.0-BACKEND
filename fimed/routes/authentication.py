from datetime import timedelta

from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED

from fimed.auth import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_active_user,
)
from fimed.model.user import UserCreateRequest, UserInDB, User, Token

router = APIRouter()


@router.post(
    "/register", name="Sing-up authentication endpoint", tags=["auth"], response_model=UserInDB,
)
async def register_to_system(user: UserCreateRequest):
    authenticated_user = authenticate_user(user.username, user.password)
    if authenticated_user:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="User already exists",
        )
    user_in_db = User.save(user)
    return user_in_db


@router.post(
    "/login", name="Login authentication endpoint", tags=["auth"], response_model=Token,
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    # print("Entro aqui y compruebo usuario")
    if not user:
        print("error de usuario")
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/me", name="Get user data", tags=["user"], response_model=UserInDB)
async def read_users_me(current_user: UserInDB = Depends(get_current_active_user)):
    #print("User: ")
    #print(current_user)
    return current_user
