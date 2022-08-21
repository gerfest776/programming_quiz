from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import EmailStr, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user.deps.auth import create_access_token, create_refresh_token
from app.api.user.deps.user import authenticate, get_user
from app.config import get_config
from app.db.database import get_session
from app.schemas.token import Token, TokenRead

router = APIRouter(prefix="/login")


@router.post("/", response_model=Token, status_code=201)
async def login(
    email: EmailStr, password: str, session: AsyncSession = Depends(get_session)
) -> Any:
    user = await authenticate(email, password, session)
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        token_type="bearer",
    )


@router.post("/refresh_token", response_model=TokenRead, status_code=201)
async def get_new_access_token(
    refresh_token: str, session: AsyncSession = Depends(get_session)
) -> Any:
    try:
        payload = jwt.decode(
            refresh_token, get_config().app.SECRET_KEY, algorithms=[get_config().app.ALGORITHM]
        )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Refresh token invalid")

    if payload["type"] == "refresh":
        user = await get_user(session, payload["sub"])
        if user.is_active:
            return TokenRead(access_token=create_access_token(payload["sub"]), token_type="bearer")
        else:
            raise HTTPException(status_code=404, detail="User inactive")
    else:
        raise HTTPException(status_code=404, detail="Incorrect token")


#
# @router.post("/login/access-token", response_model=TokenRead)
# async def login_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
# ) -> Any:
#     """
#     OAuth2 compatible token login, get an access token for future requests
#     """
#     user = await crud.user.authenticate(
#         email=form_data.username, password=form_data.password
#     )
#     if not user:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")
#     elif not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     return {
#         "access_token": security.create_access_token(
#             user.id, expires_delta=access_token_expires
#         ),
#         "token_type": "bearer",
#     }
