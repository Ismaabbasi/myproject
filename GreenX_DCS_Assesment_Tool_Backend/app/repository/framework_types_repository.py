from sqlalchemy.orm import Session, joinedload
from app.model.framework_types import FrameworkTypes
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class FrameworkTypesRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, FrameworkTypes)


    def get_all_framework_types(self):
        try: 
            with self.session_factory() as session:
                framework_types = session.query(FrameworkTypes.id, FrameworkTypes.name).order_by(FrameworkTypes.id).all()

                if framework_types is None:
                    raise ValueError("No framework types exist. Please add them to the database.")
                
                return {
                    "framework_types": framework_types 
                }
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail= f"An error occurred while retrieving the framework types from DB: {e}"
            )
            
    def get_framework_data_spider_chart(self, framework_type_id: int):
        try:
            with self.session_factory() as session:
                
                result = session.query(FrameworkTypes).options(
                    joinedload(FrameworkTypes.framework_subtype)
                ).filter(FrameworkTypes.id == framework_type_id).order_by(FrameworkTypes.id).one_or_none()

                if result is None:
                    return None
                
                return result
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail= f"An error occurred while retrieving the framework type details from DB: {e}"
            )
        
    def get_framework_type_details(self, framework_type_ids: List[int]):
        try:
            with self.session_factory() as session:
                # result = session.execute(
                #     "SELECT id, name FROM framework_types WHERE id IN :framework_type_ids",
                #     {'framework_type_ids': framework_type_ids}
                # ).fetchall()
                
                result = session.query(FrameworkTypes.id, FrameworkTypes.name).filter(FrameworkTypes.id.in_(framework_type_ids)).order_by(FrameworkTypes.id).all()

                framework_types = []
                for row in result:
                    framework_types.append({
                        "framework_type_id": row['id'],
                        "name": row['name'],
                        "framework_subtype_values": []
                    })

                return framework_types
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail= f"An error occurred while retrieving the framework type details from DB: {e}"
            )

        