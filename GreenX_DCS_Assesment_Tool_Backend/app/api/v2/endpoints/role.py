from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.core.container import Container
from typing import Dict, List

from app.core.dependencies import get_current_active_user
from app.model.user import User
from app.schema.roles_schema import RoleCreate
from app.services import RolesService

import logging

router = APIRouter(
    prefix="/role",
    tags=["role"],
)


@router.post("/create-role", response_model=dict)
@inject
def create_role(
    role_data: RoleCreate,
    # current_user: User = Depends(get_current_active_user),
    roles_service: RolesService = Depends(Provide[Container.roles_service])
):
    return roles_service.create_role(role_data)


@router.get("/get-role/{domain_id}", response_model=dict)
@inject
def get_role(
    domain_id: int,
    # current_user: User = Depends(get_current_active_user),
    roles_service: RolesService = Depends(Provide[Container.roles_service])
):
    return roles_service.get_role_types_id(domain_id)
