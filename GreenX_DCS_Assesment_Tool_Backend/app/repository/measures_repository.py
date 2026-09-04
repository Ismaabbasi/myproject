from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.model.sustainability_measures import SustainabilityMeasures
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from app.schema.measures_schema import MeasuresCreate

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class MeasuresRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, SustainabilityMeasures)
        
        
    def get_measures(self, sustainability_types_id, top_of_mind_types_id = None):
        try:
            with self.session_factory() as session:
                measures = None

                if top_of_mind_types_id is None:
                    measures = session.query(SustainabilityMeasures).filter(SustainabilityMeasures.sustainability_types_id == sustainability_types_id).all()

                else:
                    measures = session.query(SustainabilityMeasures).where(and_(SustainabilityMeasures.sustainability_types_id == sustainability_types_id, SustainabilityMeasures.top_of_mind_types_id == top_of_mind_types_id)).all()
                
                response = []
                for row in measures:
                    response.append({"id": row.id, "name": row.name})
                
                return response
            
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity issue, such as a duplicate ID or invalid foreign key."
            )
        
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid data sent to the database."
            )

        except Exception as e:
            print(f"Error while adding a domain type: {e}")

            # Rollback the transaction in case of an error
            session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )
        
    def get_typically_selected_measures(self, sustainability_types_id, top_of_mind_types_id = None):
        try:
            with self.session_factory() as session:
                
                typically_selected = None

                if top_of_mind_types_id is None:
                    typically_selected = session.execute(select(
                        SustainabilityMeasures.id, 
                        SustainabilityMeasures.name,
                        SustainabilityMeasures.description
                        ).where(and_(
                        SustainabilityMeasures.sustainability_types_id == sustainability_types_id,
                        SustainabilityMeasures.typically_selected == True
                    ))).all()

                else:
                    typically_selected = session.execute(select(
                        SustainabilityMeasures.id, 
                        SustainabilityMeasures.name,
                        SustainabilityMeasures.description
                        ).where(and_(
                        SustainabilityMeasures.sustainability_types_id == sustainability_types_id,
                        SustainabilityMeasures.top_of_mind_types_id == top_of_mind_types_id,
                        SustainabilityMeasures.typically_selected == True
                    ))).all()

                details = [{"id": row.id, "name": row.name, "description": row.description} for row in typically_selected]
                    
                return details
            
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity issue, such as a duplicate ID or invalid foreign key."
            )
        
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid data sent to the database."
            )

        except Exception as e:
            print(f"Error while adding a domain type: {e}")

            # Rollback the transaction in case of an error
            session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )

 
        
    def create_measure(self, measure_data: MeasuresCreate):
        try:
            with self.session_factory() as session:

                new_measure = SustainabilityMeasures(**measure_data.dict())
                session.add(new_measure)
                session.commit()

                return {
                    "id": new_measure.id,
                    "status": True,
                    "message": f"{new_measure.name} added successfully."
                }
            
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Data integrity issue, such as a duplicate ID or invalid foreign key while creating a new measure id: {e}"
            )
        
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid data sent to the database while creating a new measure id: {e}"
            )

        except Exception as e:
            print(f"Error while creating a new measure id: {e}")

            # Rollback the transaction in case of an error
            session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error while creating a new measure: {e}",
            )

   