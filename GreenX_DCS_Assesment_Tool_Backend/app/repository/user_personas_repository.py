from sqlalchemy.orm import Session
# from app.model.user_measures import UserSelectedMeasures
from app.model.user_selected_measures import UserSelectedMeasures

from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from app.schema.user_measures_schema import UserMeasuresCreate

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class UserPersonasRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, UserSelectedMeasures)

  

   