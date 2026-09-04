from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.model.user_selected_answers import UserSelectedAnswers

from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

# Schemas
from app.schema.user_selected_answers_schema import UserSelectedAnswersBase, UserSelectedAnswersUpdate

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class UserSelectedAnswersRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, UserSelectedAnswers)

    def delete_by_user_id(self, user_id: int):
        with self.session_factory() as session:
            query = session.query(self.model).filter(self.model.user_id == user_id).all()
            if not query:
                return
            
            for record in query:
                session.delete(record)
                
            session.commit()
            

    def save_user_answers(self, user_answers: UserSelectedAnswersBase):
        try:
            with self.session_factory() as session:

                # ID of the user selecting answers
                user_id = user_answers.user_id

                # IDS of all the answers user selected
                answer_ids = user_answers.selected_answers

                for answer_id in answer_ids:
                    answer_data = UserSelectedAnswers(
                        user_id=user_id,
                        answer_id=answer_id
                    )
                    session.add(answer_data)
                
                session.commit()

                return {
                    "status": True,
                    "message": f"User answers added successfully."
                }
            
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Data integrity issue, such as a duplicate ID or invalid foreign key while adding user answers in repository: {e}"
            )
        
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Invalid data sent to the database while adding user answers in the repository: {e}"
            )

        except Exception as e:
            print(f"Error while adding the new user answers in the repository: {e}")

            # Rollback the transaction in case of an error
            session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error while adding user answers in the repository: {e}",
            )



    def update_user_answers(self, user_id: int, user_answers: UserSelectedAnswersUpdate):
        try:
            with self.session_factory() as session:

                # IDS of all the answers user selected
                answer_ids = user_answers.selected_answers

                for answer_id in answer_ids:
                    answer_data = UserSelectedAnswers(
                        user_id=user_id,
                        answer_id=answer_id
                    )
                    session.add(answer_data)
                
                session.commit()

                return {
                    "status": True,
                    "message": f"User answers updated successfully."
                }
            
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Data integrity issue, such as a duplicate ID or invalid foreign key while updating user answers in repository: {e}"
            )
        
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Invalid data sent to the database while updating user answers in the repository: {e}"
            )

        except Exception as e:
            print(f"Error while updating user answers in the repository: {e}")

            # Rollback the transaction in case of an error
            session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error while updating user answers in the repository: {e}",
            )



    def del_previous_answers(self, user_id: int, ids_to_remove: list):
        try:
            with self.session_factory() as session:
      
                session.execute("delete from user_selected_answers where user_id = :user_id AND answer_id IN :answer_id",
                    {'user_id': user_id, 'answer_id': ids_to_remove})
                session.commit()
                return {
                    "status": True,
                    "message": f"Previous answers deleted successfully."
                }
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= f"Data integrity issue, such as a duplicate ID or invalid foreign key while deleting previous answers in repository: {e}"
            )
        
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail= f"Invalid data sent to the database while deleting previous answers in the repository: {e}"
            )

        except Exception as e:
            print(f"Error while deleting the previous answers in the repository: {e}")

            # Rollback the transaction in case of an error
            session.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error while deleting previous answers in the repository: {e}",
            )
    
    # Get all the user selected answers of a user
    def get_user_answers(self, user_id: int):
        try:
            with self.session_factory() as session:
                # user_answers = session.execute(f"select * from user_selected_answers where user_id = {user_id}").fetchall()
                user_answers = session.query(UserSelectedAnswers).filter(UserSelectedAnswers.user_id == user_id).order_by(UserSelectedAnswers.answer_id).all()

                ids = []
                for answer in user_answers:
                    ids.append(answer.answer_id)

                return ids
        except Exception as e:
            print(f"Error while getting the user selected answers in the repository: {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error while getting user selected answers in the repository: {e}",
            )
            
            
    # Get all the user selected answers of a user
    def get_user_answers_subtype(self, user_id: int, answer_ids: list):
        try:
            with self.session_factory() as session:
                # user_answers = session.execute(f"select * from user_selected_answers where user_id = {user_id}").fetchall()
                user_answers = session.query(UserSelectedAnswers).where(and_(UserSelectedAnswers.user_id == user_id, UserSelectedAnswers.answer_id.in_(answer_ids))).order_by(UserSelectedAnswers.answer_id).all()

                ids = []
                for answer in user_answers:
                    ids.append(answer.answer_id)

                return ids
        except Exception as e:
            print(f"Error while getting the user selected answers in the repository: {e}")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Internal Server Error while getting user selected answers in the repository: {e}",
            )
        


    # # Function checks if a user has a certain type of sustainability like top of mind for example
    # def user_has_measures(self, user_id: int, sustainability_measures_type_id: int):
    #     with self.session_factory() as session:
    #         user_measure = session.execute(f"select * from user_selected_measures where user_id = {user_id}").fetchall()

    #         # IDs of all the measures that the user has selected
    #         user_selected_measures = []
    #         for measure in user_measure:
    #             user_selected_measures.append(measure.sustainability_measures_id)

    #         # Check if the user has selected any measures of the defined sustainability measure type
    #         has_measure = self.user_has_measures_of_sustainability_type(selected_ids= user_selected_measures, sustainability_measures_type_id= sustainability_measures_type_id)
            
    #         return has_measure
            

    # # Function gets all the measures that the user has selected and checks if it has the defined sustainability measure type
    # def user_has_measures_of_sustainability_type(self, selected_ids: list, sustainability_measures_type_id: int):
    #     with self.session_factory() as session:
    #         for sus_id in selected_ids:
    #             measure = session.execute(f"select * from sustainability_measures where id = {sus_id} AND sustainability_types_id = {sustainability_measures_type_id}").fetchone()
    #             if measure is not None:
    #                 return True
    #         return False
        
    
    # # Filters out the ids of a particular sustainability type 
    # def user_filtered_measures_of_sustainability_type(self, selected_ids: list, sustainability_measures_type_id: int):
    #     with self.session_factory() as session:
    #         filtered_ids = []
    #         for sus_id in selected_ids:
    #             measure = session.execute(f"select * from sustainability_measures where id = {sus_id} AND sustainability_types_id = {sustainability_measures_type_id}").fetchone()
    #             if measure is not None:
    #                 filtered_ids.append(sus_id)

    #         return filtered_ids
        


        
    # def get_user_measures_id(self, user_id: int, sustainability_measures_type_id: int):
    #     try: 
    #         with self.session_factory() as session:
    #             user_exists = session.execute(f"select * from user_selected_measures where user_id = {user_id}").fetchone()

    #             if user_exists is None:
    #                 return {
    #                     "measures": [],
    #                 }
                
    #             user = session.execute(f"select * from user_selected_measures where user_id = {user_id}").fetchall()

    #             user_sustainability_measures = []
    #             for measure in user:
    #                 user_sustainability_measures.append(measure.sustainability_measures_id)

    #             measure_titles = []
    #             for measure_id in user_sustainability_measures:
    #                 measure = session.execute(f"select name from sustainability_measures where id = {measure_id} AND sustainability_types_id = {sustainability_measures_type_id}").fetchone()
    #                 if measure is not None:
    #                     measure_titles.append(measure.name)


    #             return {
    #                 "measures": measure_titles,
    #             }
            
    #     except ValueError as ve:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=str(ve)
    #         )
        
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=500, 
    #             detail= f"An error occurred while getting the user seleted measures: {e}"
    #         )
        
    # def remove_selected_ids(self, user_id: int, user_selected_ids: list):
    #     with self.session_factory() as session:
    #         for selected_id in user_selected_ids:
    #             session.execute(f"delete from user_selected_measures where user_id = {user_id} AND sustainability_measures_id = {selected_id}")
    #         session.commit()
        
        
    # def get_user_measures(self, domain_id, role_id):
    #     try:
    #         with self.session_factory() as session:
    #             print("Before getting measures")
    #             query = "SELECT id, measure, info FROM sustainability_measures WHERE domain_id = :domain_id AND role_id = :role_id"
    #             res = session.execute(query, {'domain_id': domain_id, 'role_id': role_id})
    #             print(f"After getting measures: {res}")
    #             results = res.fetchall()
    #             print(f"final results----------------------------: {results}")
    #             return results
            
    #     except IntegrityError as e:
    #         session.rollback()
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="Data integrity issue, such as a duplicate ID or invalid foreign key."
    #         )
        
    #     except DataError as e:
    #         session.rollback()
    #         raise HTTPException(
    #             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #             detail="Invalid data sent to the database."
    #         )

    #     except Exception as e:
    #         print(f"Error while adding a domain type: {e}")

    #         # Rollback the transaction in case of an error
    #         session.rollback()

    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail="Internal Server Error",
    #         )
 
        


   