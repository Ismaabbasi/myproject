from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Query

from app.core.container import Container

from app.core.dependencies import get_current_active_user
from app.model.user import User
from app.schema.user_selected_answers_schema import UserSelectedAnswersBase, UserSelectedAnswersUpdate, UserSelectedAnswersUpdateAll, QuestionAnswerUpdateDetails
from app.services import UserSelectedAnswersService


router = APIRouter(
    prefix="/user-answer",
    tags=["user-answer"],
)

# This API is used for saving the user answers. Used when all the answers have been selected.
@router.post("/save-user-answers", response_model=dict)
@inject
def save_user_answers(
    user_answers: UserSelectedAnswersBase,
    # current_user: User = Depends(get_current_active_user),
    service: UserSelectedAnswersService = Depends(Provide[Container.user_selected_answers_service])
):
    return service.save_user_answers(user_answers)


# This API is used for updating the user answers.
@router.put("/update-user-answers/{user_id}", response_model=dict)
@inject
def update_user_answers(
    user_id: int,
    user_answers: UserSelectedAnswersUpdate,
    # current_user: User = Depends(get_current_active_user),
    service: UserSelectedAnswersService = Depends(Provide[Container.user_selected_answers_service])
):
    return service.update_user_answers(user_id, user_answers)


# This API is used for updating the user answers.
@router.put("/update-user-answers-all/{user_id}", response_model=dict)
@inject
def update_user_answers_all(
    user_id: int,
    user_answers: list[QuestionAnswerUpdateDetails],
    # current_user: User = Depends(get_current_active_user),
    service: UserSelectedAnswersService = Depends(Provide[Container.user_selected_answers_service])
):
    return service.update_user_answers_all(user_id, user_answers)


# This API gives the user question answers overview based on the user id.
@router.get("/get-user-answers/{user_id}", response_model=list)
@inject
def get_user_answers(
    user_id: int,
    # current_user: User = Depends(get_current_active_user),
    service: UserSelectedAnswersService = Depends(Provide[Container.user_selected_answers_service])
):
    return service.get_user_answers(user_id)
