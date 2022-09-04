from fastapi import APIRouter, Depends

from app.api.quizz.deps.question import QuestionService
from app.schemas.quizz import QuestionCreate, QuestionRead

router = APIRouter(prefix="/question")


@router.post("/create", response_model=QuestionCreate, status_code=201)
async def create_question(question: QuestionCreate, service: QuestionService = Depends()):
    return await service.create_question(question)


@router.get("/{question_id}", response_model=QuestionRead, status_code=200)
async def get_retrieve_question(question_id: int, service: QuestionService = Depends()):
    return await service.retrieve_question(question_id)


@router.patch("/update")
def patch_question():
    pass
