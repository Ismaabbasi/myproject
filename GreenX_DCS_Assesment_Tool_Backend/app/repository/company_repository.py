from sqlalchemy.orm import Session

from sqlalchemy import insert, select

from app.model.company import Company
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from app.schema.company_schema import CompanyCreate
from app.schema.roles_schema import RoleCreate

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class CompanyRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Company)


    def get_company_id(self, company_id: int):
        try: 
            with self.session_factory() as session:
                user_company = session.execute(f"select * from company where id = {company_id}").fetchone()

                if user_company is None:
                    raise ValueError("No such id exists in the company database.")
                return user_company.name
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail="An error occurred while retrieving the company of user."
            )
        
        
    def create_company(self, company_name: str) -> dict:
        try:
            with self.session_factory() as session:
                
                # Check if the company name already exists
                companies = session.query(Company).all()
                
                for company in companies:
                    if company.name.lower() == company_name.lower():
                        return {
                            "id": company.id,
                        }
            
                # Insert the company
                session.execute(insert(Company).values(name=company_name))
                
                # Commit the transaction
                session.commit()
                
                # Get the id of the company
                new_company = session.query(Company).filter(Company.name == company_name).first()

                return {
                    "id": new_company.id,
                }
            
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data integrity issue, such as a duplicate ID or invalid foreign key while adding company data."
            )
        
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid data sent to the database for company."
            )

        except Exception as e:
            print(f"Error while adding company data: {e}")

            # Rollback the transaction in case of an error
            session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error while adding data of company{e}",
            )
        
        
    def delete_company(self, company_id: int) -> None:
        try:
            with self.session_factory() as session:
                # Check if the company exists
                company = session.execute(f"SELECT * FROM company WHERE id = {company_id}").fetchone()
                if company is None:
                    raise ValueError("No such id exists in the company database.")

                # Delete the company
                session.execute(f"DELETE FROM company WHERE id = {company_id}")
                session.commit()

        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the company."
            )
        

    def update_company_name(self, company_id: int, new_name: str) -> None:
        try:
            with self.session_factory() as session:
                # Check if the company exists
                company = session.execute(f"SELECT * FROM company WHERE id = {company_id}").fetchone()
                if company is None:
                    raise ValueError("No such id exists in the company database.")

                # Update the company name
                session.execute(f"UPDATE company SET name = '{new_name}' WHERE id = {company_id}")
                session.commit()

        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the company name."
            )

   