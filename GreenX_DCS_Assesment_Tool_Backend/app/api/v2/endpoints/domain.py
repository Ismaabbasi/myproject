from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.core.container import Container
from typing import Dict, List

from app.core.dependencies import get_current_active_user
from app.model.user import User
from app.schema.domain_schema import DomainCreate
from app.services import DomainService

import logging

router = APIRouter(
    prefix="/domain",
    tags=["domain"],
)

@router.get("/get-domain", response_model=dict)
@inject
def get_domain(
    # current_user: User = Depends(get_current_active_user),
    domain_service: DomainService = Depends(Provide[Container.domain_service])
):
    return domain_service.get_domain()

@router.post("/create-domain", response_model=dict)
@inject
def create_domain(
    domain_data: DomainCreate,
    # current_user: User = Depends(get_current_active_user),
    domain_service: DomainService = Depends(Provide[Container.domain_service])
):
    return domain_service.create_domain(domain_data)


# @router.post("/create-comment", response_model=dict)
# @inject
# def create_comment(
#     comment_data: CommentCreate,
#     # current_user: User = Depends(get_current_active_user),
#     comment_service: CommentService = Depends(Provide[Container.comment_service])
# ):
#     return comment_service.create_comment(comment_data)


# @router.delete("/delete-comment/{comment_id}", response_model=dict)
# @inject
# def delete_comment(
#     comment_id: int,
#     # current_user: User = Depends(get_current_active_user),
#     comment_service: CommentService = Depends(Provide[Container.comment_service])
# ):
#     return comment_service.delete_comment(comment_id)


# @router.put("/update-comment/{comment_id}", response_model=dict)
# @inject
# def update_comment(
#     comment_id: int,
#     comment: str,
#     # current_user: User = Depends(get_current_active_user),
#     comment_service: CommentService = Depends(Provide[Container.comment_service])
# ):
#     return comment_service.update_comment(comment_id, comment)

