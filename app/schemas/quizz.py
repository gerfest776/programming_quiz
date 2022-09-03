from pydantic import BaseModel

from app.db.models.quizz import AnswerBase, Difficulty, Language, QuestionBase


class GameToken(BaseModel):
    token: str


class GameBody(BaseModel):
    language: Language
    difficulty: Difficulty


class AnswerCreate(AnswerBase):
    pass


class QuestionCreate(QuestionBase):
    answers: list[AnswerCreate]


class QuestionRead(QuestionBase):
    id: int
