from sqlalchemy.orm import Session
from app.repository.roles_repository import RolesRepository
from app.repository import MeasuresRepository, TopOfMindTypesRolesRepository, UserProfileRepository, UserMeasuresRepository

from app.schema.roles_schema import GetRolesResponse, RoleBase, RoleCreate
from app.schema.measures_schema import MeasuresCreate, GetMeasuresByDomainIdResponse, MeasuresData, GetMeasuresResponse, TypicallySelectedMeasures

from app.services.base_service import is_valid_name, is_valid_description
from fastapi import HTTPException, status
import traceback

import logging


"""
    - There are six insights we have to give the user.
    - The insights are based on the user selected measures.
    
    Here are the insights:
    
    DONE!
    1) Of industry CTO align with your CTO's value drivers, positioning you at the forefront of sustainability thought leadership.

    What it means:
    Compare the value drivers from same role people from all companies. 

    DONE !
    Ongoing
    2) Alignment on top of mind within the team here which signifies a cohesive strategy and shared mission.

    What it means:
    How similar top of mind is with people of all roles within the user's company.


    3) Of industry financial leaders follow different value drivers, suggesting a potential deviation from prevalent sustainable financial practices.

    What it means:
    How different are the user's value drivers from the domain finance all roles.

    4) Of operations leaders in your domain share similar operational value drivers, aligning you with the pioneers of sustainable operations.

    What it means:
    How similar are the user's value drivers from the domain operation all roles.

    5) Of sustainability leaders in your sector reflect the same value drivers as your sustainability officer.

    What it means:
    How similar are the user's value drivers from the domain sustainability all roles.

    6) Of sustainability leaders in the sector have differing top of mind from your sustainability officer, suggesting realignment with industry norms.

    What it means:
    How different are top of mind of your company sustainability officer from other companies sustainability officer.
"""


class InsightService:
    def __init__(self, measures_repository: MeasuresRepository, top_of_mind_types_roles_repository: TopOfMindTypesRolesRepository, user_profile_repository: UserProfileRepository, user_measures_repository: UserMeasuresRepository):
        self.measures_repository = measures_repository
        self.top_of_mind_types_roles_repository = top_of_mind_types_roles_repository
        self.user_profile_repository = user_profile_repository
        self.user_measures_repository = user_measures_repository

    # This function fetches the selected measures of all the users ids in the list and returns the list containing an inner list of the selected measures of each user.
    def get_selected_measures(self, sustainability_type: int, user_ids: list):
        all_selected_measures = []
        
        for user_id in user_ids:
            selected_measures = self.user_measures_repository.get_user_measures_id_all_just_id(user_id, sustainability_type)
            all_selected_measures.append(selected_measures)
            
        return all_selected_measures
    
    def cal_similar_percentage(self, user_selected_measures: list, other_users_selected_measures: list):
        try:
            # Now we have the selected measures of the main user and the other users
            # We can now compare the selected measures of the main user with the other users
            
            if user_selected_measures is None or len(user_selected_measures) == 0:
                return 0
            
            # First convert to set for intersection operation
            user_selected_measures = set(user_selected_measures)
            
            total_similarity = 0
            for user in other_users_selected_measures:
                other_user_measures = set(user)
                intersection = user_selected_measures.intersection(other_user_measures)
                similarity_percentage = (len(intersection) / len(user_selected_measures)) * 100
                total_similarity += similarity_percentage
            
            average_similarity = total_similarity / len(other_users_selected_measures) if len(other_users_selected_measures) > 0 else 0
            
            average_similarity = int(average_similarity)
            
            return average_similarity
            

        except Exception as e:
            logging.error(f"Error calculating similarity percentage: {e}")
            raise e

    def calc_same_role_value_driver_similarity(self, user_id: int):
        pass
        # Get the user profile only the ids foreign keys in the table
        user_profile = self.user_profile_repository.get_user_profile_just_ids(user_id)
        
        role_id = user_profile.get("role_id")
        
        # Get all the users with the same role from all companies
        users = self.user_profile_repository.get_users_by_role_id(role_id)
        
        # Get only the ids of other users and exlcude the id of the user to compare the measures with
        other_user_ids = [user.user_id for user in users if user.user_id != user_id]
        
        # Get the selected measures of the main user
        user_selected_measures = self.get_selected_measures(2, [user_id])[0]
        
        # Get the selected measures of the other users
        other_users_selected_measures = self.get_selected_measures(2, other_user_ids)
        
        
        result = self.cal_similar_percentage(user_selected_measures, other_users_selected_measures)
        
        return result
    
    
    def calc_top_of_mind_alignment(self, user_id: int):
        pass
    
        # First get the role of the user
        user_profile = self.user_profile_repository.get_user_profile_just_ids(user_id)
        
        # Get the role id
        role_id = user_profile.get("role_id")
        company_id = user_profile.get("company_id")
        
        # Now get the other users with the same role in the company
        users = self.user_profile_repository.get_users_by_role_id_company(role_id, company_id)
        
        # Just get the ids of the users
        other_user_ids = [user.user_id for user in users if user.user_id != user_id]
        
        # Get the selected measures of the main user
        user_selected_measures = self.get_selected_measures(1, [user_id])[0]
        
        # Get the selected measures of the other users
        other_users_selected_measures = self.get_selected_measures(1, other_user_ids)
        
        result = self.cal_similar_percentage(user_selected_measures, other_users_selected_measures)
        
        return result


    def calc_financial_value_drivers_difference(self, user_id: int):
        # Get the user profile of all the roles from the finance domain in all companies
        users = self.user_profile_repository.get_users_by_domain_id(domain_id=5)
        
        # Just get the ids of the users
        other_user_ids = [user.user_id for user in users if user.user_id != user_id]
        
        # Get the selected measures of the main user
        user_selected_measures = self.get_selected_measures(2, [user_id])[0]
        
        # Get the selected measures of the other users
        other_users_selected_measures = self.get_selected_measures(2, other_user_ids)
        
        result = self.cal_similar_percentage(user_selected_measures, other_users_selected_measures)
        
        # As we are calculating the difference we will subtract the result from 100
        result = 100 - result
        
        return result
    
    
    def calc_operational_value_drivers_similarity(self, user_id: int):
        # Get the user profile of all the roles from the operation domain in all companies
        users = self.user_profile_repository.get_users_by_domain_id(domain_id=4)
        
        # Just get the ids of the users
        other_user_ids = [user.user_id for user in users if user.user_id != user_id]
        
        # Get the selected measures of the main user
        user_selected_measures = self.get_selected_measures(2, [user_id])[0]
        
        # Get the selected measures of the other users
        other_users_selected_measures = self.get_selected_measures(2, other_user_ids)
        
        result = self.cal_similar_percentage(user_selected_measures, other_users_selected_measures)
        
        return result
    
    
    def calc_sustainability_value_drivers_similarity(self, user_id: int):
        # Get the user profile of all the roles from the sustainability domain in all companies
        users = self.user_profile_repository.get_users_by_domain_id(domain_id=2)
        
        # Just get the ids of the users
        other_user_ids = [user.user_id for user in users if user.user_id != user_id]
        
        # Get the selected measures of the main user
        user_selected_measures = self.get_selected_measures(2, [user_id])[0]
        
        # Get the selected measures of the other users
        other_users_selected_measures = self.get_selected_measures(2, other_user_ids)
        
        result = self.cal_similar_percentage(user_selected_measures, other_users_selected_measures)
        
        return result
    

    def calc_sustainability_officer_top_of_mind_difference(self, user_id: int):
        
        # Get the company of the user
        user_profile = self.user_profile_repository.get_user_profile_just_ids(user_id)
        
        # Get the id of the company
        role_id = 9 # Sustainability officer role  is 9 in DB
        company_id = user_profile.get("company_id")
        
        # Now get the other users with the same role in the company
        user_company_officers = self.user_profile_repository.get_users_by_role_id_company(role_id, company_id)
        
        # Check if the user's company has a sustainability officer
        if len(user_company_officers) >= 1:
            user_company_officer = user_company_officers[0]
        else:
            return 100
        
        # Get all the user profiles of the role sustainability officer from all companies
        users = self.user_profile_repository.get_users_by_role_id(role_id)
        
        # Just get the ids of the other users excluding the user to compare with
        other_user_ids = [user.user_id for user in users if user.user_id != user_company_officer.user_id]
        
        # Get the selected measures of the sustainability officer
        user_selected_measures = self.get_selected_measures(1, [user_company_officer.user_id])[0]
        
        # Get the selected measures of the other users
        other_users_selected_measures = self.get_selected_measures(1, other_user_ids)
        
        result = self.cal_similar_percentage(user_selected_measures, other_users_selected_measures)
        
        # As we are calculating the difference we will subtract the result from 100
        result = 100 - result
        
        return result


    def get_insights(self, user_id: int):
        try:
            
            same_role_value_driver_similarity = self.calc_same_role_value_driver_similarity(user_id)
            
            top_of_mind_alignment = self.calc_top_of_mind_alignment(user_id)
            
            financial_value_drivers_difference = self.calc_financial_value_drivers_difference(user_id)
            
            operational_value_drivers_similarity = self.calc_operational_value_drivers_similarity(user_id)
            
            sustainability_value_drivers_similarity = self.calc_sustainability_value_drivers_similarity(user_id)
            
            sustainability_officer_top_of_mind_difference = self.calc_sustainability_officer_top_of_mind_difference(user_id)
            
            return {
                
                "same_role_value_driver_similarity": same_role_value_driver_similarity,
                "top_of_mind_alignment": top_of_mind_alignment,
                "financial_value_drivers_difference": financial_value_drivers_difference,
                "operational_value_drivers_similarity": operational_value_drivers_similarity,
                "sustainability_value_drivers_similarity": sustainability_value_drivers_similarity,
                "sustainability_officer_top_of_mind_difference": sustainability_officer_top_of_mind_difference
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
    
    

