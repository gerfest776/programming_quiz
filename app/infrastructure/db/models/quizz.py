from datetime import datetime
from enum import Enum
from uuid import UUID

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.models.base import Base


class BaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class QuestionAnswer(Base):
    __tablename__ = 'question_answer'

    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'), primary_key=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey('answers.id'), primary_key=True)
    is_correct: Mapped[bool] = mapped_column(nullable=False, default=False)

    question: Mapped['Question'] = relationship(back_populates="question_answer")
    answer: Mapped['Answer'] = relationship(back_populates="answer_question")


class QuestionCategory(BaseModel):
    __tablename__ = 'question_category'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    title: Mapped[str]
    questions: Mapped[list['Question']] = relationship(back_populates="category")


class Question(BaseModel):
    __tablename__ = 'questions'

    class QuestionType(Enum):
        MULTI_CHOICE = 'MULTI_CHOICE'
        SINGLE_CHOICE = 'SINGLE_CHOICE'

    class QuestionDifficulty(Enum):
        BEGINNER = 'BEGINNER'
        MEDIUM = 'MEDIUM'
        ADVANCED = 'ADVANCED'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    type: Mapped[QuestionType]
    difficult: Mapped[QuestionDifficulty]
    text: Mapped[str]

    category_id: Mapped[int] = mapped_column(ForeignKey("question_category.id"))
    category: Mapped['QuestionCategory'] = relationship(back_populates="questions")

    answers: Mapped[list['Answer']] = relationship(
        secondary='question_answer', back_populates="questions"
    )


class Answer(BaseModel):
    __tablename__ = 'answers'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    text: Mapped[str]
    questions: Mapped[list['Question']] = relationship(
        secondary='question_answer', back_populates="answers"
    )
