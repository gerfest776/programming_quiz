from fastapi import APIRouter

router = APIRouter(prefix="/question")


@router.post("/create")
def create_question():
    pass


@router.patch("/update")
def patch_question():
    pass
