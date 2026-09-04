from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container

from app.core.dependencies import get_current_active_user
from app.model.user import User
from app.schema.user_profile_schema import UserProfileCreate
from app.services import UserProfileService


router = APIRouter(
    prefix="/user-profile",
    tags=["user-profile"],
)

@router.post("/create-user-profile", response_model=dict, status_code=status.HTTP_201_CREATED)
@inject
def create_user_profile(
    user_profile_data: UserProfileCreate,
    # current_user: User = Depends(get_current_active_user),
    service: UserProfileService = Depends(Provide[Container.user_profile_service])
):
    return service.create_user_profile(user_profile_data)


@router.get("/get-user-profile/{user_id}", response_model=dict)
@inject
def get_user_profile(
    user_id: int,
    # current_user: User = Depends(get_current_active_user),
    service: UserProfileService = Depends(Provide[Container.user_profile_service])
):
    return service.get_user_profile_by_user_id(user_id)
