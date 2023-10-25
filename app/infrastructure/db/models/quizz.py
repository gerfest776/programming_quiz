from datetime import datetime
from enum import Enum
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class QuestionAnswer(Base):
    __tablename__ = 'question_answer'

    question: Mapped["Question"] = mapped_column(primary_key=True)
    answer: Mapped["Answer"] = mapped_column(primary_key=True)
    is_correct: Mapped[bool] = mapped_column(nullable=False, default=False)


class Question(BaseModel):
    __tablename__ = 'questions'

    class QuestionType(Enum):
        MULTI_CHOICE = 'MULTI_CHOICE'
        SINGLE_CHOICE = 'SINGLE_CHOICE'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    type: Mapped[QuestionType]
    text: Mapped[str]
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

