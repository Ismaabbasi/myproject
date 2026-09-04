from sqlalchemy.orm import Session
from app.model.strengths import Strengths
from app.schema.domain_schema import DomainCreate
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from fastapi import HTTPException, status

class StrengthsRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Strengths)

