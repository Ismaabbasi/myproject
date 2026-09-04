from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.model.other_measures import OtherMeasures
from app.schema.domain_schema import DomainCreate
from app.repository.base_repository import BaseRepository
from app.core.exceptions import DuplicatedError, NotFoundError
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from fastapi import HTTPException, status

class OtherMeasuresRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, OtherMeasures)
        
        
    def save_other_measure(self, schema):
        with self.session_factory() as session:
            
            measure_exists = self.get_other_measures(schema.user_id, schema.sustainability_types_id)
            
            # Updating the measure if a measure of same sustainability type exists
            if measure_exists:
                updated_measure = self.update(measure_exists.id, schema)
                return updated_measure
                
            query = self.model(**schema.dict())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return query
        
    def get_other_measures(self, user_id, sustainability_types_id):
        with self.session_factory() as session:
            measures = session.query(OtherMeasures).where(and_(OtherMeasures.user_id == user_id, OtherMeasures.sustainability_types_id == sustainability_types_id)).one_or_none()
            return measures
        
    def get_other_measures_all(self, user_id):
        with self.session_factory() as session:
            measures = session.query(OtherMeasures).filter(OtherMeasures.user_id == user_id).all()
            return measures

