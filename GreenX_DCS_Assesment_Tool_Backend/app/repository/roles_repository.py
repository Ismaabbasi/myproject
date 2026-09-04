from sqlalchemy.orm import Session
from app.model.roles import Roles
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from app.schema.roles_schema import RoleCreate

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class RolesRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Roles)

    def get_role_types(self):
        with self.session_factory() as session:
            print("Before getting roles")
            res = session.execute("select * from roles")
            print(f"After getting domain types: {res}")
            results = res.fetchall()
            print(f"final results: {results}")
            return {
                "results": results,
            }
        
    def get_role_by_id(self, role_id: int):
        try: 
            with self.session_factory() as session:
                role = session.execute(f"select * from roles where id = {role_id}").fetchone()

                if role is None:
                    raise ValueError("No such id exists in the role table.")
                return {
                    "role_name": role.name,
                }
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail= f"An error occurred while retrieving the role: {e}"
            )
        
        
    def get_role_types_id(self, domain_id):
        with self.session_factory() as session:
            print("Before getting roles")
            # res = session.execute(f"select * from roles where domain_type_id = {domain_id}")
            results = session.query(Roles).filter(Roles.domain_type_id == domain_id).all()
            # print(f"After getting domain types: {res}")
            # results = res.fetchall()
            # print(f"final results: {results}")
            return {
                "results": [result.__dict__ for result in results]
            }
        
    def create_role(self, role_type_data: RoleCreate):
        try:
            with self.session_factory() as session:

                new_role_type = Roles(**role_type_data.dict())

                session.add(new_role_type)
                session.commit()

                return {
                    "id": new_role_type.id,
                    "domain_type_id": new_role_type.domain_type_id,
                    "name": new_role_type.name,
                }
            
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

   