from sqlalchemy.orm import Session
from app.model.answers import Answers
from app.repository.base_repository import BaseRepository
from typing import Callable, Dict, List
from contextlib import AbstractContextManager
from sqlmodel import select

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

class AnswersRepository(BaseRepository):
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        super().__init__(session_factory, Answers)


    def get_all_answers(self, question_ids: List[int]):
        try: 
            with self.session_factory() as session:
                answers = session.query(Answers.id, Answers.questions_id, Answers.answer, Answers.weight).filter(Answers.questions_id.in_(question_ids)).order_by(Answers.id).all()
                    
                if answers is None:
                    raise ValueError("No such id exists in the table of answers.")
                
                return {
                    "answers": answers 
                }
            
        except ValueError as ve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(ve)
            )
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail= f"An error occurred while retrieving the answers from DB: {e}"
            )
        
    def get_answer_details(self, answer_ids: List[int]):
        try:
            with self.session_factory() as session:
                result = session.query(Answers.id, Answers.questions_id, Answers.answer).filter(Answers.id.in_(answer_ids)).all()

                answers = []
                for row in result:
                    answers.append({
                        "answer_id": row['id'],
                        "questions_id": row['questions_id'],
                        "answer": row['answer']
                    })

                return answers

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while retrieving the answers from DB: {e}"
            )
        

    def get_question_type_id(self, answer_ids: list):
        try:
            with self.session_factory() as session:
                # Use parameterized query to prevent SQL injection
                questions = session.execute(
                    "SELECT questions_id FROM answers WHERE id IN :answer_ids",
                    {'answer_ids': answer_ids}
                ).fetchall()

                # Extract the questions_id values from the result
                questions_ids = [question['questions_id'] for question in questions]

                # Check if the list is empty
                if not questions_ids:
                    raise ValueError("No questions_id found in the database.")

                # Check if all the questions_id are similar
                if not all(q_id == questions_ids[0] for q_id in questions_ids):
                    raise ValueError("Not all questions_id are the same.")

                return questions_ids[0]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while retrieving the answers from DB: {e}"
            )

    def get_ids_of_same_question_old_answers(self, question_type: int, previous_answers: list):
        try:
            with self.session_factory() as session:

                # Use parameterized query to prevent SQL injection
                ids = session.execute(
                    "SELECT id FROM answers WHERE questions_id = :question_type AND id IN :previous_answers",
                    {'question_type': question_type, 'previous_answers': previous_answers}
                ).fetchall()
                
                # Extract the id values from the result
                ids = [id['id'] for id in ids]

                return ids

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while retrieving the answer ids from DB: {e}"
            )
        