import uuid

from db.database import get_session
from db.models import Question
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import redis
from app.schemas.quizz import GameBody, GameToken

router = APIRouter(prefix="/quizz")


@router.post("/start", response_model=GameToken, status_code=201)
async def start_quizz(game_conf: GameBody, session: AsyncSession = Depends(get_session)):
    question_order = session.get(Question, {**game_conf})
    await redis.set(token := uuid.uuid4().hex, game_conf.json(), 3600)
    return {"token": token}
