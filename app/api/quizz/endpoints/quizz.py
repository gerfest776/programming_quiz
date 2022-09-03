import json
import random
import uuid

from db.database import get_session
from db.models import Question
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import redis
from app.schemas.quizz import GameBody, GameToken

router = APIRouter(prefix="/quizz")


@router.post("/start", response_model=GameToken, status_code=201)
async def start_quizz(game_conf: GameBody, session: AsyncSession = Depends(get_session)):
    statement = select(Question.id).filter_by(**game_conf.dict())
    question_order = [i[0] for i in (await session.execute(statement)).all()]
    random.shuffle(question_order)
    game_data = {"questions": question_order, **game_conf.dict()}
    await redis.set(token := uuid.uuid4().hex, json.dumps(game_data), 3600)
    return {"token": token}
