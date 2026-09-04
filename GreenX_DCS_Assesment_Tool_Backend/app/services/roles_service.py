from sqlalchemy.orm import Session
from app.repository.roles_repository import RolesRepository
from app.schema.roles_schema import GetRolesResponse, RoleBase, RoleCreate, RoleGet

from app.services.base_service import is_valid_name
from fastapi import HTTPException, status
import traceback

import logging

class RolesService:
    def __init__(self, roles_repository: RolesRepository):
        self.roles_repository = roles_repository

    def get_role_types(self):
        try:
            print("Getting roles")
            results = self.roles_repository.get_role_types()["results"]
            roles = [RoleBase(**result) for result in results]
            logging.info(f"This the result being received from repo: {roles}")
            return GetRolesResponse(roles=roles)
        except Exception as e:
            logging.error(f"Error getting roles: {e}")
            raise e
    
        
    def get_role_types_id(self, domain_id):
        try:
            print("Getting roles from id")
            results = self.roles_repository.get_role_types_id(domain_id)["results"]
            roles = [RoleGet(**result) for result in results]
            logging.info(f"This the result being received from repo: {roles}")
            return GetRolesResponse(roles=roles)
        except Exception as e:
            logging.error(f"Error getting roles: {e}")
            raise e
    
        
    def create_role(self, role_data: RoleCreate):
        try:
            return self.roles_repository.create_role(role_data)
    
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )
    

