from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.quizz import Answer, Question
from app.schemas.quizz import QuestionCreate, QuestionRead


class QuestionService:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def create_question(self, question: QuestionCreate) -> QuestionCreate:
        question_obj = Question.from_orm(question)
        self.session.add(question_obj)
        await self.session.commit()

        for answer in question.answers:
            answer.question_id = question_obj.id
            self.session.add(Answer.from_orm(answer))
        await self.session.commit()

        await self.session.refresh(question_obj)

        return question

    async def retrieve_question(self, question_id: int) -> QuestionRead:
        question = await self.session.get(Question, question_id)
        statement = select(Answer).where(Answer.question_id == question.id)
        return QuestionRead(
            id=question.id,
            answers=[i[0].text for i in (await self.session.execute(statement)).all()]
            + question.fake_answers,
        )

    async def check_question(self, question_id: int, answers: list[str]) -> bool:
        statement = select(Answer).where(Answer.question_id == question_id)
        right_answers = [i[0].text for i in (await self.session.execute(statement)).all()]
        if answers == right_answers:
            return True
        return False
