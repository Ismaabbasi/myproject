from sqlalchemy.orm import Session

from app.model.top_of_mind_roles import TopOfMindRoles
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from app.schema.roles_schema import RoleCreate

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class TopOfMindTypesRolesRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, TopOfMindRoles)

    def get_top_of_mind_types_id(self, role_id):
        try:
          with self.session_factory() as session:
            res = session.query(TopOfMindRoles).filter(TopOfMindRoles.role_id == role_id).one_or_none()

            if res is None:
                # raise ValueError("No such role id exists in the database.")
                return 8
            
            return res.top_of_mind_types_id
        
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"An error occurred while retrieving the top of mind types from role id: {e}"
            )

