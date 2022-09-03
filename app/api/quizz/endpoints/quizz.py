import uuid

from fastapi import APIRouter

from app.db.redis import redis
from app.schemas.quizz import GameBody, GameToken

router = APIRouter(prefix="/quizz")


@router.post("/start", response_model=GameToken, status_code=201)
async def start_quizz(game_conf: GameBody):
    await redis.set(token := uuid.uuid4().hex, game_conf.json(), 3600)
    return {"token": token}
