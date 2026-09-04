from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload
from app.model.user_profile import UserProfile
from app.schema.user_profile_schema import UserProfileids
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select
from app.core.exceptions import NotFoundError
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class UserProfileRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, UserProfile)

    def get_user_profile(self):
        try:
            with self.session_factory() as session:
                # res = session.execute("select * from user_profiles")
                results = session.query(UserProfile).options(
                    joinedload(UserProfile.user),
                    joinedload(UserProfile.company),
                    joinedload(UserProfile.domain_type),
                    joinedload(UserProfile.roles)
                ).all()
                
                # results = res.fetchall()
                
                return {
                    "results": results,
                }
        except Exception as e:
            print(f"Error while getting all user profiles: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error while getting all user profiles: {e}",
            )
            
    def get_user_profile_just_ids(self, user_id: int):
        try:
            with self.session_factory() as session:
                user = session.query(UserProfile).filter(UserProfile.user_id == user_id).one_or_none()
                
                if user is None:
                    return {}
                
                return {
                    "id": user.id,
                    "user_id": user.user_id,
                    "company_id": user.company_id,
                    "domain_id": user.domain_id,
                    "role_id": user.role_id
                }
            
        except Exception as e:
            print(f"Error while getting user profile just ids: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error while getting user profile just ids: {e}",
            )
            
    def get_users_by_role_id(self, role_id: int):
        try:
            with self.session_factory() as session:
                users = session.query(UserProfile).filter(UserProfile.role_id == role_id).all()
                
                if users is None:
                    return []
                
                return users
            
        except Exception as e:
            print(f"Error while getting users by role id: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error while getting users by role id: {e}",
            )
            
    # Get all users by a particular domain id with an optional company id
    def get_users_by_domain_id(self, domain_id: int, company_id: int = -1): 
        try:
            with self.session_factory() as session:
    
                if company_id == -1:
                    users = session.query(UserProfile).filter(UserProfile.domain_id == domain_id).all()
                    
                else:
                    users = session.query(UserProfile).where(and_(UserProfile.domain_id == domain_id, UserProfile.company_id == company_id)).all()
                
                if users is None:
                    return []
                
                return users
            
        except Exception as e:
            print(f"Error while getting users by role id: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error while getting users by role id: {e}",
            )
            
    
    def get_users_by_role_id_company(self, role_id: int, company_id: int):
        try:
            with self.session_factory() as session:
                users = session.query(UserProfile).where(and_(UserProfile.role_id == role_id, UserProfile.company_id == company_id)).all()
                
                if users is None:
                    return []
                
                return users
            
        except Exception as e:
            print(f"Error while getting users by role id: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error while getting users by role id: {e}",
            )
    
    
    def get_user_profile_by_user_id(self, user_id: int):
        try: 
            with self.session_factory() as session:
                
                user_profile = session.query(UserProfile).options(
                    joinedload(UserProfile.user),
                    joinedload(UserProfile.company),
                    joinedload(UserProfile.domain_type),
                    joinedload(UserProfile.roles)
                ).filter(UserProfile.user_id == user_id).one_or_none()
            
            
                if user_profile is None:
                    return None
            
                
                return user_profile
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail= f"An error occurred while retrieving the user profile: {e}"
            )
        
    def user_profile_exists(self, user_profile_id) -> bool:
        try:
            with self.session_factory() as session:
                statement = select(UserProfile).where(UserProfile.user_id == user_profile_id)
                results = session.execute(statement).first()
                return results is not None
        except Exception as e:
            print(f"Error while checking if user profile exists: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error while checking if user profile exists: {e}",
            )


    def create_user_profile(self, user_profile: UserProfileids) -> dict:
        try:
            with self.session_factory() as session:

                # Check if the user id already exists
                user_id = user_profile["user_id"]

                if self.user_profile_exists(user_id):
                    # Delete the existing user profile
                    session.execute(f"delete from user_profiles where user_id = {user_id}")
                    session.commit()

                new_user_profile = UserProfile(**user_profile)
                session.add(new_user_profile)
                session.commit()
                
                return {
                    "id": new_user_profile.id,
                    "user_id": new_user_profile.user_id,
                    "company_id": new_user_profile.company_id,
                    "domain_id": new_user_profile.domain_id,
                    "role_id": new_user_profile.role_id
                }
            
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Data integrity issue, such as a duplicate ID or invalid foreign key while creating user profile: {e}"
            )
        
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Invalid data sent to the database while creating user profile: {e}"
            )
        
        except Exception as e:
            print(f"Error while creating user profile in repository: {e}")
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error while creating user profile: {e}",
            )
        
    def get_domain_and_role_id(self, user_id: int):
        try:
            with self.session_factory() as session:
                user_profile = session.execute(f"select * from user_profiles where user_id = {user_id}").fetchone()

                if user_profile is None:
                    raise ValueError("No such user id exists in the user profile table.")

                return {
                    "domain_id": user_profile.domain_id,
                    "role_id": user_profile.role_id
                }
        
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
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
            print(f"Error while creating user profile in repository: {e}")
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error while getting user domain and role id: {e}",
            )
            
    def delete_user_profile(self, user_id: int):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.user_id == user_id).first()
            if not query:
                raise NotFoundError(detail=f"not found id : {user_id}")
            session.delete(query)
            session.commit()
            
            return query
        


        