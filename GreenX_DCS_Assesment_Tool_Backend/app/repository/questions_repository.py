from sqlalchemy.orm import Session
from app.model.questions import Questions
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class QuestionsRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Questions)


    def get_all_questions(self, framework_subtype_ids: List[int]):
        try: 
            with self.session_factory() as session:
                questions = session.query(Questions.id, Questions.framework_subtypes_id, Questions.is_single_choice, Questions.question).filter(Questions.framework_subtypes_id.in_(framework_subtype_ids)).order_by(Questions.id).all()

                if questions is None:
                    raise ValueError("No questions exist. Please add them to the database.")
                
                return {
                    "questions": questions 
                }
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail= f"An error occurred while retrieving the questions from DB: {e}"
            )
            
    def get_questions_subtype_id(self, subtype_id: int):
        try: 
            with self.session_factory() as session:
                questions = session.query(Questions.id, Questions.framework_subtypes_id, Questions.is_single_choice, Questions.question).filter(Questions.framework_subtypes_id == subtype_id).order_by(Questions.id).all()

                if questions is None:
                    return {}
                
                return questions
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail= f"An error occurred while retrieving the questions from DB: {e}"
            )

        
    def get_question_details(self, question_ids: List[int]):
        try:
            with self.session_factory() as session:                
                result = session.query(Questions.id, Questions.framework_subtypes_id, Questions.is_single_choice, Questions.question).filter(Questions.id.in_(question_ids)).order_by(Questions.id).all()

                questions = []
                for row in result:
                    questions.append({
                        "question_id": row['id'],
                        "framework_subtypes_id": row['framework_subtypes_id'],
                        "question": row['question'],
                        "is_single_choice": row['is_single_choice'],
                        "answer_values": []
                    })

                return questions
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail= f"An error occurred while retrieving the questions from DB: {e}"
            )
        
        


        