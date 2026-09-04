from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundError
from app.model import UserSelectedMeasures, SustainabilityMeasures

from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from app.schema.user_measures_schema import UserMeasuresCreate

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

import traceback

class UserMeasuresRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, UserSelectedMeasures)


    # Function checks if a user has a certain type of sustainability like top of mind for example
    def user_has_measures(self, user_id: int, sustainability_measures_type_id: int):
        with self.session_factory() as session:
            user_measure = session.execute(f"select * from user_selected_measures where user_id = {user_id}").fetchall()

            # IDs of all the measures that the user has selected
            user_selected_measures = []
            for measure in user_measure:
                user_selected_measures.append(measure.sustainability_measures_id)

            # Check if the user has selected any measures of the defined sustainability measure type
            has_measure = self.user_has_measures_of_sustainability_type(selected_ids= user_selected_measures, sustainability_measures_type_id= sustainability_measures_type_id)
            
            return has_measure
            

    # Function gets all the measures that the user has selected and checks if it has the defined sustainability measure type
    def user_has_measures_of_sustainability_type(self, selected_ids: list, sustainability_measures_type_id: int):
        with self.session_factory() as session:
            for sus_id in selected_ids:
                measure = session.execute(f"select * from sustainability_measures where id = {sus_id} AND sustainability_types_id = {sustainability_measures_type_id}").fetchone()
                if measure is not None:
                    return True
            return False
        
    
    # Filters out the ids of a particular sustainability type 
    def user_filtered_measures_of_sustainability_type(self, selected_ids: list, sustainability_measures_type_id: int):
        with self.session_factory() as session:
            filtered_ids = []
            for sus_id in selected_ids:
                measure = session.execute(f"select * from sustainability_measures where id = {sus_id} AND sustainability_types_id = {sustainability_measures_type_id}").fetchone()
                if measure is not None:
                    filtered_ids.append(sus_id)

            return filtered_ids
        
    # This is a function just like get_user_measures_id but it returns the measure titles, id etc instead of just names of selected measures
    def get_user_measures_id_all(self, user_id: int, sustainability_measures_type_id: int):
        try: 
            with self.session_factory() as session:
                user_exists = session.execute(f"select * from user_selected_measures where user_id = {user_id}").fetchone()

                if user_exists is None:
                    return {
                        "measures": [],
                    }
                
                user = session.execute(f"select * from user_selected_measures where user_id = {user_id}").fetchall()

                user_sustainability_measures = []
                for measure in user:
                    user_sustainability_measures.append(measure.sustainability_measures_id)

                measures = []
                for measure_id in user_sustainability_measures:
                    if sustainability_measures_type_id == 1:
                        measure = session.execute(f"select id, sustainability_types_id, top_of_mind_types_id from sustainability_measures where id = {measure_id} AND sustainability_types_id = {sustainability_measures_type_id}").fetchone()
                        if measure is not None:
                            measures.append({
                                "id": measure.id,
                                "sustainability_types_id": measure.sustainability_types_id,
                                "top_of_mind_types_id": measure.top_of_mind_types_id
                            })
                    
                    else:
                        measure = session.execute(f"select id, sustainability_types_id from sustainability_measures where id = {measure_id} AND sustainability_types_id = {sustainability_measures_type_id}").fetchone()
                        if measure is not None:
                            measures.append({
                                "id": measure.id,
                                "sustainability_types_id": measure.sustainability_types_id,
                            })


                return measures
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail= f"An error occurred while getting the user seleted measures: {e}"
            )

        
    def get_user_measure(self, user_id: int, sustainability_measures_type_id: int):
        try: 
            with self.session_factory() as session:
                user = session.query(UserSelectedMeasures).filter(UserSelectedMeasures.user_id == user_id).all()

                if user is None:
                    return {
                        "measures": [],
                    }

                user_sustainability_measures = []
                for measure in user:
                    user_sustainability_measures.append(measure.sustainability_measures_id)

                measure_titles = []
                for measure_id in user_sustainability_measures:
                    measure = session.query(SustainabilityMeasures).where(and_(SustainabilityMeasures.id == measure_id, SustainabilityMeasures.sustainability_types_id == sustainability_measures_type_id)).one_or_none()
                    if measure is not None:
                        measure_titles.append(measure.name)

                return {
                    "measures": measure_titles,
                }
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail= f"An error occurred while getting the user seleted measures: {e}"
            )
        
    def remove_selected_ids(self, user_id: int, user_selected_ids: list):
        with self.session_factory() as session:
            for selected_id in user_selected_ids:
                session.execute(f"delete from user_selected_measures where user_id = {user_id} AND sustainability_measures_id = {selected_id}")
            session.commit()
        # with self.session_factory() as session:
        #     query = session.query(self.model).filter(self.model.user_id.in_(user_selected_ids))
        #     if not query:
        #         raise NotFoundError(detail=f"not found ids : {user_selected_ids}")
        #     session.delete(query)
        #     session.commit()
            
        #     return query
        
        
    def get_user_measures(self, domain_id, role_id):
        try:
            with self.session_factory() as session:
                print("Before getting measures")
                query = "SELECT id, measure, info FROM sustainability_measures WHERE domain_id = :domain_id AND role_id = :role_id"
                res = session.execute(query, {'domain_id': domain_id, 'role_id': role_id})
                print(f"After getting measures: {res}")
                results = res.fetchall()
                print(f"final results----------------------------: {results}")
                return results
            
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
 
        
    def save_user_measure(self, measure_data: UserMeasuresCreate):
        try:
            with self.session_factory() as session:

                # Getting all the user selected measures previously selected
                user_id = measure_data.user_id
                user_old_measures = session.execute(f"select * from user_selected_measures where user_id = {user_id}").fetchall()

                # Putting the sustainability measures ids from user selected measures in a list
                user_old_measures_ids = []
                if user_old_measures is not None:
                    for measure in user_old_measures:
                        user_old_measures_ids.append(measure.sustainability_measures_id)

                # Only get the sustainability measures ids of the current sustainability type like for example top of mind
                filtered_measure_ids = []
                if user_old_measures_ids is not None:
                    filtered_measure_ids = self.user_filtered_measures_of_sustainability_type(selected_ids= user_old_measures_ids, sustainability_measures_type_id= measure_data.sustainability_types_id)

                # Remove the old measures that the user has selected
                if filtered_measure_ids is not None:  
                    self.remove_selected_ids(user_id= user_id, user_selected_ids= filtered_measure_ids)


                # All the new measures id user selected
                sustainability_ids = measure_data.measures

                # Adding the new measures to the user_selected_measures table
                for sustainability_id in sustainability_ids:
                    measure_data = UserSelectedMeasures(
                        user_id=user_id,
                        sustainability_measures_id=sustainability_id
                    )
                    session.add(measure_data)
                
                session.commit()

                return {
                    "status": True,
                    "message": f"Sustainability measures added successfully."
                }
            
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Data integrity issue, such as a duplicate ID or invalid foreign key while adding user measures: {e}"
            )
        
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Invalid data sent to the database while adding user measures: {e}"
            )

        except Exception as e:
            print(f"Error while adding the new measure: {e}")

            # Rollback the transaction in case of an error
            session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error while adding user measures: {e}",
            )

   
   
   
    # This is a function just like get_user_measures_id but it returns the measure titles, id etc instead of just names of selected measures
    def get_user_measures_id_all_just_id(self, user_id: int, sustainability_measures_type_id: int):
        try: 
            with self.session_factory() as session:
                # user_exists = session.execute(f"select * from user_selected_measures where user_id = {user_id}").fetchone()
                user = session.query(UserSelectedMeasures).filter(UserSelectedMeasures.user_id == user_id).all()

                if len(user) == 0:
                    return {
                        "measures": [],
                    }
                
                # user = session.execute(f"select * from user_selected_measures where user_id = {user_id}").fetchall()

                user_sustainability_measures = []
                for measure in user:
                    user_sustainability_measures.append(measure.sustainability_measures_id)

                measures = []
                for measure_id in user_sustainability_measures:
                    # measure = session.execute(f"select id, sustainability_types_id from sustainability_measures where id = {measure_id} AND sustainability_types_id = {sustainability_measures_type_id}").fetchone()
                    measure_id = session.query(SustainabilityMeasures.id).where(and_(SustainabilityMeasures.id == measure_id, SustainabilityMeasures.sustainability_types_id == sustainability_measures_type_id)).one_or_none()
                    if measure_id is not None:
                        measures.append(measure_id.id)


                return measures
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(traceback_str)
            raise HTTPException(
                status_code=500, 
                detail= f"An error occurred while getting the user seleted measures: {e}"
            )