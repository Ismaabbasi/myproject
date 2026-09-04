from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.core.container import Container
from typing import Dict, List

from app.core.dependencies import get_current_active_user
from app.model.user import User

from app.schema.feedback_schema import FeedbackCreate

from app.services import FeedbackService

import logging

router = APIRouter(
    prefix="/feedback",
    tags=["Feedback APIs - For strenghts and improvements after Spider Chart"],
)


@router.post("/create-feedback", response_model=str)
@inject
def create_feedback(
    feedback_data: FeedbackCreate,
    # current_user: User = Depends(get_current_active_user),
    feedback_service: FeedbackService = Depends(Provide[Container.feedback_service])
):
    return feedback_service.create_feedback(feedback_data)


# @router.delete("/delete-feedback/{feedback_id}", response_model=dict)
# @inject
# def delete_feedback(
#     feedback_id: int,
#     # current_user: User = Depends(get_current_active_user),
#     feedback_service: FeedbackService = Depends(Provide[Container.feedback_service])
# ):
#     return feedback_service.delete_comment(feedback_id)


# @router.put("/update-feedback/{comment_id}", response_model=dict)
# @inject
# def update_feedback(
#     feedback_id: int,
#     feedback_data: str,
#     # current_user: User = Depends(get_current_active_user),
#     feedback_service: FeedbackService = Depends(Provide[Container.feedback_service])
# ):
#     return feedback_service.update_comment(feedback_id, feedback_data)

