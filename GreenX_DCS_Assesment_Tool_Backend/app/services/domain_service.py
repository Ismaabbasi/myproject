from sqlalchemy.orm import Session
from app.repository.domain_repository import DomainRepository
from app.schema.domain_schema import DomainCreate
from app.schema.domain_schema import GetDomainResponse, DomainBase, DomainGet, DomainCreate

from app.services.base_service import is_valid_name
from fastapi import HTTPException, status
import traceback

import logging

class DomainService:
    def __init__(self, domain_repository: DomainRepository):
        self.domain_repository = domain_repository

    def get_domain(self) -> GetDomainResponse:
        try:
            results = self.domain_repository.get_domain()["results"]
            domain = [DomainGet(**result) for result in results]
            return GetDomainResponse(domain=domain)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"An error occured while fetching the domains. Please try again later.{e}"
            )
    
    def create_domain(self, domain_data: DomainCreate):
        try:
            result = self.domain_repository.create(domain_data)
            result_dict = result.__dict__
            domain = DomainGet(**result_dict)
            return domain
    
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occured in creating the domain. Please try again later.{e}"
            )

    def create_domain_type(self, domain_type_data: DomainCreate):
        try:
            is_domain_name_valid = is_valid_name(domain_type_data.name)
            is_domain_descr_valid = is_valid_name(domain_type_data.description)

            if not is_domain_name_valid or not is_domain_descr_valid:
                raise ValueError("Invalid domain name or description.") 
            
            return self.domain_repository.create_domain_type(domain_type_data)
        
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )
