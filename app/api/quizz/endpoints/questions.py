from fastapi import APIRouter, Depends

from app.api.quizz.deps.question import QuestionService
from app.schemas.quizz import QuestionCreate

router = APIRouter(prefix="/question")


@router.post("/create", response_model=QuestionCreate, status_code=201)
async def create_question(question: QuestionCreate, service: QuestionService = Depends()):
    return await service.create_question(question)


@router.patch("/update")
def patch_question():
    pass
