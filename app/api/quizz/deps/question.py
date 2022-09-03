from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.quizz import Answer, Question
from app.schemas.quizz import QuestionCreate


class QuestionService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_question(self, question: QuestionCreate) -> QuestionCreate:
        [self.session.add(Answer.from_orm(answer)) for answer in question.answers]
        await self.session.commit()
        question_obj = Question.from_orm(question)
        self.session.add(question_obj)
        await self.session.commit()

        for answer in question.answers:
            answer.question_id = question_obj.id
            self.session.add(Answer.from_orm(answer))
        await self.session.commit()

        await self.session.refresh(question_obj)

        return question
