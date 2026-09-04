from sqlalchemy.orm import Session
# from app.model.user_measures import UserSelectedMeasures
from app.model.user_selected_measures import UserSelectedMeasures

from app.repository.base_repository import BaseRepository
from typing import Callable
from contextlib import AbstractContextManager


class QuestionAnswerRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, UserSelectedMeasures)

  

   