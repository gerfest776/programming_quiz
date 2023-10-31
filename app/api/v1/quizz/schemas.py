from pydantic import BaseModel

from app.utils import QuestionDifficulty, QuestionType


class Category(BaseModel):
    title: str


class Answer(BaseModel):
    text: str
    is_right: bool


class Question(BaseModel):
    text: str
    type: QuestionType
    difficult: QuestionDifficulty
    categories: list[Category]
    answers: list[Answer]


class QuestionList(BaseModel):
    questions: list[Question]
