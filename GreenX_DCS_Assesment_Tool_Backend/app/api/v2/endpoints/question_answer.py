from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Query

from app.core.container import Container

from app.core.dependencies import get_current_active_user
from app.model.user import User
from app.schema.question_answer_schema import GetSubtypeQuestionAnswers
from app.services import QuestionAnswerService


router = APIRouter(
    prefix="/question-answer",
    tags=["question-answer"],
)

# This API gives you all the framework subtypes, subtype's questions and their respective answers as response.
@router.get("/get-all-question-answer", response_model=dict)
@inject
def get_all_question_answer(
    # current_user: User = Depends(get_current_active_user),
    service: QuestionAnswerService = Depends(Provide[Container.question_answer_service])
):
    return service.get_all_question_answer()


# This API gives the specific questions and answers when subtype id is provided.
@router.post("/subtype-questions-answers", response_model=dict)
@inject
def get_subtype_questions_answers(
    subtype_data: GetSubtypeQuestionAnswers,
    # current_user: User = Depends(get_current_active_user),
    service: QuestionAnswerService = Depends(Provide[Container.question_answer_service])
):
    return service.get_questions_answers_subtype(subtype_data)
