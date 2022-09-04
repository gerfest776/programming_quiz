import json
import random
import uuid

from api.quizz.deps.question import QuestionService
from db.database import get_session
from db.models import Question
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import check_token, redis
from app.schemas.quizz import AnswerCheck, GameBody, GameToken, QuestionRead

router = APIRouter(prefix="/quizz")


@router.post("/start", response_model=GameToken, status_code=201)
async def start_quizz(game_conf: GameBody, session: AsyncSession = Depends(get_session)):
    statement = select(Question.id).filter_by(**game_conf.dict())
    question_order = [i[0] for i in (await session.execute(statement)).all()]
    random.shuffle(question_order)
    token_data = json.dumps({"order": question_order})
    await redis.set(token := uuid.uuid4().hex, token_data, 3600)
    return {"token": token}


@router.get("/", response_model=QuestionRead, status_code=200)
async def get_question_token(token: str, service: QuestionService = Depends()):
    token_data = await check_token(token)
    return await service.retrieve_question(token_data["order"][0])


@router.post("/check", response_model=GameToken, status_code=200)
async def check_question_answer(
    answers: AnswerCheck, token: str, service: QuestionService = Depends()
):
    token_data = await check_token(token)
    if await service.check_question(token_data["order"][0], answers.answers):
        del token_data["order"][0]
        if not token_data["order"]:
            await redis.delete(token)
            raise HTTPException(status_code=404, detail="Game Finished")
        await redis.set(token, json.dumps(token_data), 3600)
        return {"token": token}
    await redis.delete(token)
    raise HTTPException(status_code=400, detail="Wrong answer")
