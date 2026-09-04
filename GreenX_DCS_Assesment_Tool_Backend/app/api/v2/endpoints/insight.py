from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Query

from app.core.container import Container

from app.core.dependencies import get_current_active_user
from app.model.user import User
from app.schema.user_selected_answers_schema import UserSelectedAnswersBase, UserSelectedAnswersUpdate
from app.services import InsightService


router = APIRouter(
    prefix="/insight",
    tags=["Insight & Analysis - User selected measure comparison with other users"],
)

# This API is used for saving the user answers. Used when all the answers have been selected.
@router.get("/get-insights/{user_id}", response_model=dict)
@inject
def get_insights(
    user_id: int,
    # current_user: User = Depends(get_current_active_user),
    insight_service: InsightService = Depends(Provide[Container.insight_service])
):
    return insight_service.get_insights(user_id)


