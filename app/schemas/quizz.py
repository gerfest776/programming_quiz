from pydantic import BaseModel

from app.db.models.quizz import Difficulty, Language


class GameToken(BaseModel):
    token: str


class GameBody(BaseModel):
    language: Language
    difficulty: Difficulty
