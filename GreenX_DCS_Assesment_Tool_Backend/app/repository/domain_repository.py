from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.model.domain_types import DomainTypes
from app.schema.domain_schema import DomainCreate
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from fastapi import HTTPException, status

class DomainRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, DomainTypes)

    def get_domain(self):
        with self.session_factory() as session:
            # results = session.query(DomainTypes).all()
            # results = session.query(DomainTypes).filter(or_(DomainTypes.created_by_id.is_(None), DomainTypes.created_by_id == user_id)).order_by(DomainTypes.created_by_id).all()
            results = session.query(DomainTypes).order_by(DomainTypes.id).all()
            return {
                 "results": [result.__dict__ for result in results]
            }

    def get_domain_by_id(self, domain_id: int):
        try: 
            with self.session_factory() as session:
                domain = session.execute(f"select * from domain_types where id = {domain_id}").fetchone()

                if domain is None:
                    raise ValueError("No such id exists in the domain table.")

                print(f"This is the domain: {domain}")
                return {
                    "domain_name": domain.name,
                }
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail= f"An error occurred while retrieving the domain: {e}"
            )

    

    def create_domain_type(self, domain_type_data: DomainCreate):

        try:
            with self.session_factory() as session:
                existing_domain_type = session.execute(select(DomainTypes).where(DomainTypes.name == domain_type_data.name)).first()
                if existing_domain_type:
                    raise ValueError(f"Domain type with name '{domain_type_data.name}' already exists.")

                new_domain_type = DomainTypes(**domain_type_data.dict())

                session.add(new_domain_type)
                session.commit()

                return {
                    "domain_type_id": new_domain_type.id,
                    "name": new_domain_type.name,
                    "description": new_domain_type.description,
                }
        except Exception as e:
            print(f"Error while adding a domain type: {e}")

            # Rollback the transaction in case of an error
            session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error",
            )

