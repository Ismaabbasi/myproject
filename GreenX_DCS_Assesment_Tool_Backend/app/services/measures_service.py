from sqlalchemy.orm import Session
from app.repository.roles_repository import RolesRepository
from app.repository import MeasuresRepository, TopOfMindTypesRolesRepository

from app.repository.user_measures_repository import UserMeasuresRepository

from app.schema.roles_schema import GetRolesResponse, RoleBase, RoleCreate
from app.schema.measures_schema import MeasuresCreate, GetMeasuresByDomainIdResponse, MeasuresData, GetMeasuresResponse, TypicallySelectedMeasures

from app.services.base_service import is_valid_name, is_valid_description
from fastapi import HTTPException, status
import traceback

import logging

class MeasuresService:
    def __init__(self, measures_repository: MeasuresRepository, top_of_mind_types_roles_repository= TopOfMindTypesRolesRepository):
        self.measures_repository = measures_repository
        self.top_of_mind_types_roles_repository = top_of_mind_types_roles_repository


    def compare_user_measure_id(self, user_id: int):
        try:
            # # Check if user has selected all 3 measures
            user_measures_repo = UserMeasuresRepository(session_factory=self.measures_repository.session_factory)

            has_top_of_minds = user_measures_repo.user_has_measures(user_id= user_id, sustainability_measures_type_id=  1)
            has_value_drivers = user_measures_repo.user_has_measures(user_id= user_id, sustainability_measures_type_id=  2)
            has_main_challenges = user_measures_repo.user_has_measures(user_id= user_id, sustainability_measures_type_id=  3)

            if not has_top_of_minds or not has_value_drivers or not has_main_challenges:
                return {
                    "top_of_mind_similar": None,
                    "top_of_mind_difference": None,
                    "value_driver_similar": None,
                    "value_driver_difference": None,
                    "main_challenges_similar": None,
                    "main_challenges_difference": None
                }
            

            # first get the user selected measures
            top_of_mind = user_measures_repo.get_user_measures_id_all(user_id, 1)

            top_of_mind_ids_list = []

            # Append the ids to a list as name not required
            for top in top_of_mind:
                top_of_mind_ids_list.append(top["id"])

            # We are getting the top of mind type based on the first item in the list as everyone will have the same type which user selected)
            top_of_mind_type = top_of_mind[0]["top_of_mind_types_id"]

            # Getting type of top of mind based on role id through the top of mind types role repository
            typically_top_of_mind = self.measures_repository.get_typically_selected_measures(sustainability_types_id = 1, top_of_mind_types_id = top_of_mind_type)

            typically_top_of_mind_ids_list = []

            for top in typically_top_of_mind:
                typically_top_of_mind_ids_list.append(top["id"])

            top_of_mind_similar = self.cal_similarity_percentage(user_selected_measures=top_of_mind_ids_list, typically_selected_measures=typically_top_of_mind_ids_list)


            # For value drivers
            value_driver = user_measures_repo.get_user_measures_id_all(user_id, 2)

            value_driver_ids_list = []

            # Append the ids to a list as name not required
            for value in value_driver:
                value_driver_ids_list.append(value["id"])

            # Getting type of top of mind based on role id through the top of mind types role repository
            typically_value_drivers = self.measures_repository.get_typically_selected_measures(sustainability_types_id = 2)

            typically_value_drivers_list = []

            for value in typically_value_drivers:
                typically_value_drivers_list.append(value["id"])

            value_drivers_similar = self.cal_similarity_percentage(user_selected_measures=value_driver_ids_list, typically_selected_measures=typically_value_drivers_list)

            # For main challenges
            main_challenges = user_measures_repo.get_user_measures_id_all(user_id, 3)

            main_challenges_ids_list = []

            # Append the ids to a list as name not required
            for challenge in main_challenges:
                main_challenges_ids_list.append(challenge["id"])

            # Getting type of top of mind based on role id through the top of mind types role repository
            typically_main_challenges = self.measures_repository.get_typically_selected_measures(sustainability_types_id = 3)

            typically_main_challenges_list = []

            for challenge in typically_main_challenges:
                typically_main_challenges_list.append(challenge["id"])

            main_challenges_similar = self.cal_similarity_percentage(user_selected_measures=main_challenges_ids_list, typically_selected_measures=typically_main_challenges_list)


            return {
                "top_of_mind_similar": top_of_mind_similar,
                "top_of_mind_difference": 100 - top_of_mind_similar,
                "value_driver_similar": value_drivers_similar,
                "value_driver_difference": 100 - value_drivers_similar,
                "main_challenges_similar": main_challenges_similar,
                "main_challenges_difference": 100 - main_challenges_similar
            }
        
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )


        except Exception as e:
            logging.error(f"Error comparing user selected measures: {e}")
            raise e
        
    def cal_similarity_percentage(self, user_selected_measures: list, typically_selected_measures: list):
        try:
            # compare the two lists
            # get the length of the two lists
            # get the number of similar items in the two lists
            # calculate the percentage of similarity

            total = len(typically_selected_measures)
            similar = 0

            for measure in user_selected_measures:
                if measure in typically_selected_measures:
                    similar += 1

            try:
                percentage = (similar / total) * 100
                return int(percentage)
            except ZeroDivisionError:
                return 0
            

        except Exception as e:
            logging.error(f"Error calculating similarity percentage: {e}")
            raise e
    
    # This function is used to get measures for the top of mind, value drivers and main challenges page.
    def get_measures(self, measure_data: GetMeasuresByDomainIdResponse):
        try:
            sustainability_types_id = measure_data.sustainability_types_id
            role_id = measure_data.role_id

            # Used if users wants to get top of mind measures which are based on the role of the user
            top_of_mind_type = None
            if role_id is not None:
                top_of_mind_type = self.top_of_mind_types_roles_repository.get_top_of_mind_types_id(role_id)

            # Used to get top of mind, value drivers and main challenges measures based on requested sustainability type
            measures = self.measures_repository.get_measures(sustainability_types_id = sustainability_types_id, top_of_mind_types_id = top_of_mind_type)

            # Used to get typically selected measures based on requested sustainability type
            typically_selected = self.measures_repository.get_typically_selected_measures(sustainability_types_id = sustainability_types_id, top_of_mind_types_id = top_of_mind_type)

            return GetMeasuresResponse(measures=measures, typically_selected_measures=typically_selected)
        
        except Exception as e:
            logging.error(f"Error getting top of mind measures: {e}")
            raise e
    
        
    def create_measure(self, measure_data: MeasuresCreate):
        try:
            is_title_valid = is_valid_description(measure_data.measure)
            is_info_valid = is_valid_description(measure_data.info)

            if not is_title_valid or not is_info_valid:
                raise ValueError("Invalid measure type. Please use allowed characters.")
            
            new_measure = self.measures_repository.create_measure(measure_data)
            return new_measure
    
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )
    

