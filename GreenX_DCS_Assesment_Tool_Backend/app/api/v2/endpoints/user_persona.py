from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Query

from app.core.container import Container

from app.core.dependencies import get_current_active_user
from app.model.user import User
from app.schema.user_profile_schema import UserProfileCreate
from app.services import UserPersonasService


router = APIRouter(
    prefix="/user-persona",
    tags=["user-persona"],
)

# Get the user personas of the user using user id from user profile
@router.post("/get-persona-one", response_model=dict)
@inject
def get_persona_one(
    user_id: int = Query(..., title="User ID", description="The ID of the user."),
    current_user: User = Depends(get_current_active_user),
    service: UserPersonasService = Depends(Provide[Container.user_personas_service])
):
    return service.get_user_persona_one(user_id)


@router.get("/get-persona-all", response_model=list)
@inject
def get_persona_all(
    current_user: User = Depends(get_current_active_user),
    service: UserPersonasService = Depends(Provide[Container.user_personas_service])
):
    return service.get_user_personas_all(current_user.id)

