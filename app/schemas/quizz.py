from pydantic import BaseModel

from app.db.models.quizz import AnswerBase, Difficulty, Language, QuestionBase


class GameToken(BaseModel):
    token: str


class GameBody(BaseModel):
    language: Language
    difficulty: Difficulty


class QuestionCreate(QuestionBase):
    answers: list[AnswerBase]


class QuestionRead(BaseModel):
    id: int
    answers: list[str]


class AnswerCheck(BaseModel):
    answers: list[str]
