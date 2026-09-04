from datetime import datetime
from app.schema.user_profile_schema import UserProfileBase
import logging

from app.repository import UserPersonasRepository, OtherMeasuresRepository
from app.repository.roles_repository import RolesRepository
from app.repository.user_repository import UserRepository
from app.repository.company_repository import CompanyRepository
from app.repository.domain_repository import DomainRepository
from app.repository.user_measures_repository import UserMeasuresRepository
from app.repository.user_profile_repository import UserProfileRepository


class UserPersonasService:
    def __init__(self, user_personas_repository: UserPersonasRepository, user_profile_repository: UserProfileRepository, other_measures_repository: OtherMeasuresRepository):
        self.user_personas_repository = user_personas_repository
        self.user_profile_repository = user_profile_repository
        self.other_measures_repository = other_measures_repository
        

    def get_user_personas_all(self, user_id: int):
        try:
            # Getting all the user profiles
            results = self.user_profile_repository.get_user_profile()["results"]

            # Getting the company name of the user with the provided user id
            # We do this so we could get the personas of users with the same company as the user
            company_name = ""
            for result in results:
                if result.user.id == user_id:
                    company_name = result.company.name
                    break
                
            if company_name == "":
                return []

            # Getting the user ids from the profiles
            user_ids = []
            for user_profile in results:
                user_ids.append(user_profile.user.id)

            # Reverse the list to get the latest profile persona first
            user_ids.reverse()

            # Getting the user personas for each user id
            user_personas = []
            for user_id in user_ids:
                persona = self.get_user_persona_one(user_id)
                    
                if persona != {} and len(persona.get("main_challenges")) > 0 and company_name.lower() in persona["profile"]["Company"].lower() and (datetime.now() - persona["profile"]["created_at"]).days < 2:
                    user_personas.append(persona)

            return user_personas
        
        except Exception as e:
            logging.error(f"Error while making user personas overall: {e}")
            raise e
        
    def get_user_persona_one(self, user_id: int):
        try:
            # Getting the user profile from the provided user_id in order to get the ids for domain, role, company
            result = self.user_profile_repository.get_user_profile_by_user_id(user_id)
            
            if result is None:
                return {}

            # Getting the user name and email from the user id in result
            name = result.user.name
            email = result.user.email

            # Getting the domain name from the domain id in result
            domain_name = result.domain_type.name

            # Getting the role name from the role id in result
            role_name = result.roles.name

            # Getting the company name from the company id in result
            company_name = result.company.name
            
            # Created_at and updated_at of the user profile
            created_at = result.created_at
            updated_at = result.updated_at

            # Getting the user selected measures            
            user_measures_repo = UserMeasuresRepository(session_factory=self.user_personas_repository.session_factory)
            top_of_mind = user_measures_repo.get_user_measure(user_id, 1)["measures"]
            value_drivers = user_measures_repo.get_user_measure(user_id, 2)["measures"]
            main_challenges = user_measures_repo.get_user_measure(user_id, 3)["measures"]
            
            # Now getting the user other measures
            other_measures = self.other_measures_repository.get_other_measures_all(user_id)
            
            # Adding the other measures to the top of mind, value drivers and main challenges lists.
            for measure in other_measures:
                other_measure = measure.other_measure
                if measure.sustainability_types_id == 1:
                    top_of_mind.append(other_measure)
                elif measure.sustainability_types_id == 2:
                    value_drivers.append(other_measure)
                elif measure.sustainability_types_id == 3:
                    main_challenges.append(other_measure)

            # Initials of the name in capital letters
            name_parts = name.split()
            # Extract the first letter of each part and join them
            initials = ''.join([part[0] for part in name_parts if part]).upper()

            return {
            "profile": {
                "name": name,
                "initials": initials,
                "email": email,
                "Company": company_name,
                "domain": domain_name,
                "role": role_name,
                "created_at": created_at,
                "updated_at": updated_at
            },
            "top_of_mind": top_of_mind,
            "value_drivers": value_drivers,
            "main_challenges": main_challenges  
            } 
        
        except Exception as e:
            logging.error(f"Error getting User personas one in service: {e}")
            raise e