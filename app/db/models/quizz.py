from enum import Enum

from sqlalchemy.schema import Column
from sqlmodel import ARRAY, Field, Relationship, SQLModel, String


class Language(str, Enum):
    PYTHON = "python"
    GO = "go"
    JAVASCRIPT = "javascript"
    JAVA = "java"
    RUBY = "ruby"
    PHP = "php"


class Difficulty(str, Enum):
    JUNIOR = "junior"
    MIDDLE = "middle"
    SENIOR = "senior"


class QuestionType(str, Enum):
    MULTIPLE = "multiple"
    SINGLE = "single"


class QuestionBase(SQLModel):
    difficulty: Difficulty
    language: Language
    type: QuestionType
    text: str
    fake_answers: list[str] = Field(sa_column=Column(ARRAY(String)))


class AnswerBase(SQLModel):
    text: str
    description: str
    question_id: int | None = Field(default=None, foreign_key="question.id")


class Question(QuestionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    answers: list["Answer"] = Relationship(back_populates="question")


class Answer(AnswerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question: Question | None = Relationship(back_populates="answers")
