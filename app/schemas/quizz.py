from pydantic import BaseModel

from app.db.models.quizz import Difficulty, Language, QuestionType


class GameToken(BaseModel):
    token: str


class GameBody(BaseModel):
    language: Language
    difficulty: Difficulty


class Answer(BaseModel):
    text: str
    description: str


class Question(BaseModel):
    text: str
    answers: str


class CreateQuestion(BaseModel):
    difficulty: Difficulty
    language: Language
    type: QuestionType
    text: str
    fake_answers: list[str]
    right_answers: list[Answer]
