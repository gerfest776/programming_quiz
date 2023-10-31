from app.infrastructure.db.models import Answer, Question
from app.infrastructure.repositories.base import BaseAlchemyRepository


class AnswerRepository(BaseAlchemyRepository[Answer]):
    model = Answer


class QuestionRepository(BaseAlchemyRepository[Question]):
    model = Question



