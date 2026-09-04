from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container

from app.core.dependencies import get_current_active_user
from app.model.user import User
from app.schema.user_measures_schema import UserMeasuresCreate, GetUserSelectedMeasuresData
from app.services import UserMeasuresService


router = APIRouter(
    prefix="/user-measure",
    tags=["user-measure"],
)

@router.post("/create-user-measures", response_model=dict)
@inject
def save_measures(
    measures_data: UserMeasuresCreate,
    # current_user: User = Depends(get_current_active_user),
    service: UserMeasuresService = Depends(Provide[Container.user_measures_service])
):
    return service.save_user_measure(measures_data)


@router.post("/get-user-measures", response_model=dict)
@inject
def get_user_measures(
    user_data: GetUserSelectedMeasuresData,
    # current_user: User = Depends(get_current_active_user),
    service: UserMeasuresService = Depends(Provide[Container.user_measures_service])
):
    return service.get_user_measure(user_data)

# @router.get("/compare-measures/{user_id}", response_model=dict)
# @inject
# def compare_measures(
#     user_id: int,
#     current_user: User = Depends(get_current_active_user),
#     service: MeasuresService = Depends(Provide[Container.measures_service])
# ):
#     return service.compare_user_measure_id(user_id)



