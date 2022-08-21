from typing import Any

from fastapi import APIRouter, Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.user.deps.auth import create_access_token, create_refresh_token
from app.api.user.deps.user import authenticate
from app.db.database import get_session
from app.schemas.token import Token

router = APIRouter(prefix="/token")


@router.post("/login", response_model=Token, status_code=201)
async def login(
    email: EmailStr, password: str, session: AsyncSession = Depends(get_session)
) -> Any:
    user = await authenticate(email, password, session)
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        token_type="bearer",
    )


# @router.post(
#     "/login/refresh_token", response_model=IPostResponseBase[TokenRead], status_code=201
# )
# async def get_refresh_token(
#     body: RefreshToken = Body(...),
# ) -> Any:
#     """
#     Get Refresh token
#     """
#     try:
#         payload = jwt.decode(
#             body.refresh_token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
#         )
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(status_code=403, detail="Refresh token invalid")
#
#     if payload["type"] == "refresh":
#         access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#         user = await crud.user.get(id=payload["sub"])
#         if user.is_active:
#             access_token = security.create_access_token(
#                 payload["sub"], expires_delta=access_token_expires
#             )
#             return IPostResponseBase[TokenRead](
#                 data=TokenRead(access_token=access_token, token_type="bearer"),
#                 message="Access token generated correctly",
#             )
#         else:
#             raise HTTPException(status_code=404, detail="User inactive")
#     else:
#         raise HTTPException(status_code=404, detail="Incorrect token")
#
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
