from sqlalchemy.orm import Session
from app.repository.roles_repository import RolesRepository
from app.repository.measures_repository import MeasuresRepository
from app.repository import UserMeasuresRepository, OtherMeasuresRepository
from app.model.sustainability_measures import SustainabilityMeasures




from app.schema.roles_schema import GetRolesResponse, RoleBase, RoleCreate
from app.schema.user_measures_schema import UserMeasuresCreate, GetUserSelectedMeasuresData, OtherMeasuresCreate
from app.schema.measures_schema import MeasuresCreate, GetMeasuresByDomainIdResponse, MeasuresData, GetMeasuresResponse

from app.services.base_service import is_valid_name, is_valid_description
from fastapi import HTTPException, status
import traceback

import logging

class UserMeasuresService:
    def __init__(self, user_measures_repository: UserMeasuresRepository, other_measures_repository: OtherMeasuresRepository):
        self.user_measures_repository = user_measures_repository
        self.other_measures_repository = other_measures_repository
            
    def get_user_measure(self, user_data: GetUserSelectedMeasuresData):
        try:
            print("Getting measures based on the user id")

            user_id = user_data.user_id
            sustainability_measures_type_id = user_data.sustainability_measures_type_id

            results = self.user_measures_repository.get_user_measure(user_id, sustainability_measures_type_id)
            return results
        except Exception as e:
            logging.error(f"Error getting user selected measures: {e}")
            raise e
    

    def save_user_measure(self, measure_data: UserMeasuresCreate):
        try:

            # Check if the measure name is valid
            if measure_data.new_measure:
                is_valid = is_valid_name(measure_data.new_measure)

                if not is_valid:
                    raise ValueError("Unallowed characters used while adding new measure. Please use allowed characters.")
                
            # Check if the user already has selected measures previously
            user_measures = self.user_measures_repository.get_user_measure(measure_data.user_id, measure_data.sustainability_types_id)

            # Add the new measure to the other measures table
            if measure_data.new_measure:
                data = OtherMeasuresCreate(user_id=measure_data.user_id, sustainability_types_id=measure_data.sustainability_types_id, other_measure=measure_data.new_measure)
                self.other_measures_repository.save_other_measure(data)

            selected_measures_len = len(measure_data.measures)

            if selected_measures_len == 0:
                raise ValueError("No measures were selected.")

            new_user_measure = self.user_measures_repository.save_user_measure(measure_data)
            
            # This contains the success message
            return new_user_measure
    
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )
        except Exception as e:
            logging.error(f"Error creating measure: {e}")
            raise e
    

