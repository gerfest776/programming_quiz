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


class Question(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    difficulty: Difficulty
    language: Language
    type: QuestionType
    text: str
    fake_answers: list[str] = Field(sa_column=Column(ARRAY(String)))
    right_answers: list["RightAnswer"] = Relationship(back_populates="question")


class RightAnswer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    description: str
    question_id: int = Field(default=None, foreign_key="question.id")
    question: Question = Relationship(back_populates="right_answers")
