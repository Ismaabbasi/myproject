from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Query

from app.core.container import Container

from app.core.dependencies import get_current_active_user
from app.model.user import User
from app.schema.chart_schema import SpiderChartGet
from app.services import ChartService


router = APIRouter(
    prefix="/chart",
    tags=["Charts and Graphs"],
)

# This API is used for saving the user answers. Used when all the answers have been selected.
@router.post("/get-spider-chart", response_model=dict)
@inject
def get_spider_chart(
    chart_data: SpiderChartGet,
    # current_user: User = Depends(get_current_active_user),
    chart_service: ChartService = Depends(Provide[Container.chart_service])
):
    return chart_service.get_spider_chart(chart_data)

