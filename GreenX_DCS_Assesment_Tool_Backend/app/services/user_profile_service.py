from fastapi import HTTPException, status
from app.schema.user_profile_schema import GetUserProfileResponse, UserProfileBase, UserProfileCreate, UserProfileUpdate, UserProfileModel
import logging
import traceback

from app.repository import CompanyRepository, UserProfileRepository, UserMeasuresRepository

# import is_valid_name
from app.services.base_service import is_valid_name

class UserProfileService:
    def __init__(self, user_profile_repository: UserProfileRepository, company_repository: CompanyRepository, user_measures_repository: UserMeasuresRepository):
        self.user_profile_repository = user_profile_repository
        self.company_repository = company_repository
        self.user_measures_repository = user_measures_repository

    def get_user_profile(self):
        try:
            print("Getting profiles")
            results = self.user_profile_repository.get_user_profile()["results"]
            print(f"Results Again: {results}")
            profiles = [UserProfileBase(**result) for result in results]
            logging.info(f"This the result being received from repo: {profiles}")
            return GetUserProfileResponse(profiles=profiles)
        except Exception as e:
            logging.error(f"Error getting roles: {e}")
            raise e
        
    def get_user_profile_by_user_id(self, user_id: int):
        try:
            print("Getting user profile by id")
            user_profile = self.user_profile_repository.get_user_profile_by_user_id(user_id)
            
            # If there is no user profile which exists
            if user_profile is None:
                return {}

            # Initials of the name in capital letters
            name = user_profile.user.name
            name_parts = name.split()
            # Extract the first letter of each part and join them
            initials = ''.join([part[0] for part in name_parts if part]).upper()

            # Getting the user selected measures            
            top_of_mind = self.user_measures_repository.get_user_measure(user_id, 1)["measures"]
            value_drivers = self.user_measures_repository.get_user_measure(user_id, 2)["measures"]
            main_challenges = self.user_measures_repository.get_user_measure(user_id, 3)["measures"]

            return {
                "name": name,
                "email": user_profile.user.email if user_profile.user else "No email provided",
                "Company": user_profile.company.name if user_profile.company else "No company provided",
                "domain": user_profile.domain_type.name if user_profile.domain_type else "No domain provided",
                "role": user_profile.roles.name if user_profile.roles else "No role provided",
                "initials": initials,
                "top_of_mind": top_of_mind,
                "value_drivers": value_drivers,
                "main_challenges": main_challenges
            } 
        except Exception as e:
            logging.error(f"Error getting User profile: {e}")
            raise e

    def create_user_profile(self, user_profile_data: UserProfileCreate) -> dict:
        try:
            # Checking if the user already has a profile and if yes then deleting it
            user_id = user_profile_data.user_id
            profile_exists = self.get_user_profile_by_user_id(user_id)
            
            if profile_exists != {}:
                self.user_profile_repository.delete_user_profile(user_id)
            
            # Check if the company name is valid
            if not is_valid_name(user_profile_data.company_name):
                raise ValueError("Unallowed letters used for organization name.")
            
            # Getting the company id from the company name
            company_id = self.company_repository.create_company(user_profile_data.company_name)["id"]

            data = {
                "user_id": user_profile_data.user_id,
                "company_id": company_id,
                "domain_id": user_profile_data.domain_id,
                "role_id": user_profile_data.role_id
            }

            # print(f"This is the user profile: {user_profile_data_with_company_id}")
            
            user_profile_schema = UserProfileModel(**data)

            # Creating the user profile
            result = self.user_profile_repository.create(user_profile_schema)
            # result = self.user_profile_repository.create_user_profile(data)

            return {
                "message": f"User profile created successfully"
            }
        
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(ve)
            )

        except HTTPException as http_exc:
            raise http_exc

        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal Server Error in service."
            )
        
    # Get the domain id and role id from the user profile based on user id
    def get_domain_and_role_id(self, user_id: int):
        try:
            result = self.user_profile_repository.get_domain_and_role_id(user_id)
            return {
                "domain_id": result["domain_id"],
                "role_id": result["role_id"]
            }
        except Exception as e:
            logging.error(f"Error getting the domain and role ids of the user: {e}")
            raise e
        
    # To work on after the completion of the user measures part
    # def update_user_profile(self, user_profile_data: UserProfileUpdate) -> dict:
    #     try:
    #         # Check if the company name is valid
    #         if not is_valid_name(user_profile_data.company_name):
    #             raise ValueError("Unallowed letters used for organization name.")
            
    #         # Getting the company id from the company name
    #         company_repo = CompanyRepository(session_factory=self.user_profile_repository.session_factory)
    #         company_id = company_repo.create_company(user_profile_data.company_name)["id"]

    #         user_profile_data_with_company_id = {
    #             "user_id": user_profile_data.user_id,
    #             "company_id": company_id,
    #             "domain_id": user_profile_data.domain_id,
    #             "role_id": user_profile_data.role_id
    #         }

    #         # Updating the user profile
    #         result = self.user_profile_repository.update_user_profile(user_profile_data_with_company_id)

    #         return {
    #             "message": f"User profile with id {user_profile_data.user_id} updated successfully",
    #         }
        
    #     except ValueError as ve:
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail=str(ve)
    #         )

    #     except HTTPException as http_exc:
    #         raise http_exc

    #     except Exception as e:
    #         logging.error(f"Error updating user profile: {e}")
    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="Internal Server Error in service."
    #         )