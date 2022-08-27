from fastapi import APIRouter

from app.api.quizz.endpoints.quizz import router as quizz_router
from app.api.user.endpoints.token import router as token_router
from app.api.user.endpoints.user import router as user_router

api_router = APIRouter()

api_router.include_router(user_router, tags=["user"])
api_router.include_router(token_router, tags=["token"])
api_router.include_router(quizz_router, tags=["quizz"])
