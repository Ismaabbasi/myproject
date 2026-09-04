from sqlalchemy.orm import Session
from app.model.framework_subtypes import FrameworkSubtypes
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class FrameworkSubtypesRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, FrameworkSubtypes)


    def get_all_framework_subtypes(self, framework_type_ids: List[int]):
        try: 
            with self.session_factory() as session:
                
                # ids_str = ','.join(map(str, framework_type_ids))
                # framework_subtypes = session.execute(f"SELECT id, framework_type_id, name FROM framework_subtypes WHERE framework_type_id IN ({ids_str})").fetchall()
                framework_subtypes = session.query(FrameworkSubtypes.id, FrameworkSubtypes.framework_type_id, FrameworkSubtypes.name).filter(FrameworkSubtypes.framework_type_id.in_(framework_type_ids)).order_by(FrameworkSubtypes.id).all()

                if framework_subtypes is None:
                    raise ValueError("No such id exists in the table of framework subtypes.")
                
                return {
                    "framework_subtypes": framework_subtypes 
                }
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail= f"An error occurred while retrieving the framework subtypes from DB: {e}"
            )
        
    def get_framework_subtype_details(self, framework_subtype_ids: List[int]):
        try:
            with self.session_factory() as session:
                # result = session.execute(
                #     "SELECT id, framework_type_id, name FROM framework_subtypes WHERE id IN :framework_subtype_ids",
                #     {'framework_subtype_ids': framework_subtype_ids}
                # ).fetchall()
                
                result = session.query(FrameworkSubtypes.id, FrameworkSubtypes.framework_type_id, FrameworkSubtypes.name).filter(FrameworkSubtypes.id.in_(framework_subtype_ids)).order_by(FrameworkSubtypes.id).all()

                framework_subtypes = []
                for row in result:
                    framework_subtypes.append({
                        "framework_subtype_id": row['id'],
                        "framework_type_id": row['framework_type_id'],
                        "name": row['name'],
                        "question_values": []
                    })

                return framework_subtypes
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail= f"An error occurred while retrieving the framework subtype details from DB: {e}"
            )
        

        