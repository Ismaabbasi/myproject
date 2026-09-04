from sqlalchemy.orm import Session

from app.repository.user_selected_answers_repository import UserSelectedAnswersRepository
from app.repository.framework_types_repository import FrameworkTypesRepository
from app.repository.framework_subtypes_repository import FrameworkSubtypesRepository
from app.repository.questions_repository import QuestionsRepository
from app.repository.answers_repository import AnswersRepository

# Schemas
from app.schema.user_selected_answers_schema import UserSelectedAnswersBase, UserSelectedAnswersUpdate, QuestionAnswerUpdateDetails

from app.services.base_service import is_valid_name, is_valid_description
from fastapi import HTTPException, status
import traceback

class UserSelectedAnswersService:
    def __init__(self, user_selected_answers_repository: UserSelectedAnswersRepository, framework_types_repository: FrameworkTypesRepository, framework_subtypes_repository: FrameworkSubtypesRepository, questions_repository: QuestionsRepository, answers_repository: AnswersRepository):
        self.user_selected_answers_repository = user_selected_answers_repository
        self.framework_types_repository = framework_types_repository
        self.framework_subtypes_repository = framework_subtypes_repository
        self.questions_repository = questions_repository
        self.answers_repository = answers_repository

    # This function gets the user answers from the database
    def get_user_answers(self, user_id: int):
        try:
            
            # Sending the data to the repository to get the user selected answers
            selected_ans_ids = self.user_selected_answers_repository.get_user_answers(user_id)

            # Get the answer id, answer(string) and question id of the selected answers
            answers = []
            if len(selected_ans_ids) > 0:
                answers = self.answer_details(selected_ans_ids)

            # Get the question id, question (string) and subtype id of the selected answer's questions
            questions = []
            if len(answers) > 0:
                # Only get the question_ids from the answers
                question_ids = [answer["questions_id"] for answer in answers]
                questions = self.question_details(question_ids)

            # Get the id, subtype (string) and framework type id of the selected answer question's subtypes
            subtypes = []
            if len(questions) > 0:
                # Only get the subtype_ids from the questions
                subtype_ids = [question["framework_subtypes_id"] for question in questions]
                subtypes = self.subtype_details(subtype_ids)

            # Get the id, type (string) of the selected answer question's subtype's framework type
            framework_types = []
            if len(subtypes) > 0:
                # Only get the framework_type_ids from the subtypes
                framework_type_ids = [subtype["framework_type_id"] for subtype in subtypes]
                framework_types = self.framework_type_details(framework_type_ids)

            # Make the final response by combining all the data in a proper linked way
            all_data = {
                "answers": answers,
                "questions": questions,
                "subtypes": subtypes,
                "framework_types": framework_types
            }

            response = self.link_user_selected_q_ans_subtype_framework(all_data)


            return response

        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while fetching selected answers: {e}"
            )
        
    # This function links the user selected answers, questions, subtypes and framework types in a proper way
    def link_user_selected_q_ans_subtype_framework(self, all_data: dict):
        try:
            # Get the answers, questions, subtypes and framework types
            answers = all_data["answers"]
            questions = all_data["questions"]
            subtypes = all_data["subtypes"]
            framework_types = all_data["framework_types"]

            result = []

            # First add the framework types
            for framework_type in framework_types:
                result.append(framework_type)

            # Now add the subtypes and link them with the framework types. If the ids match, add the subtype to the framework type framework subtypes values list of each framework.
            for subtype in subtypes:
                for framework_type in result:
                    if subtype["framework_type_id"] == framework_type["framework_type_id"]:
                        framework_type["framework_subtype_values"].append(subtype)

            # Now add the questions and link them with the subtypes. If the ids match, add the question to the subtype question values list of each subtype.
            # After getting home, continue with the same logic for questions.
            for question in questions:
                for framework in result:
                    for subtype in framework["framework_subtype_values"]:
                        if question["framework_subtypes_id"] == subtype["framework_subtype_id"]:
                            subtype["question_values"].append(question)

            # Now add the answers and link them with the questions. If the ids match, add the answer to the question answer values list of each question.
            for answer in answers:
                for framework in result:
                    for subtype in framework["framework_subtype_values"]:
                        for question in subtype["question_values"]:
                            if answer["questions_id"] == question["question_id"]:
                                question["answer_values"].append(answer)
            
            return result

          

        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while linking selected answers, questions, subtypes and framework types: {e}"
            )
        
    # This function gives the answer id, answer(string) and question id of the selected answers
    def answer_details(self, selected_ans_ids: list):
        try:
            answers = self.answers_repository.get_answer_details(selected_ans_ids)

            return answers
        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while fetching answers: {e}"
            )
        
    # This function gives the question id, question (string) and subtype id of the selected answer's questions
    def question_details(self, question_ids: list):
        try:
            questions = self.questions_repository.get_question_details(question_ids)

            return questions
        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while fetching questions: {e}"
            )
        
    def subtype_details(self, subtype_ids: list):
        try:
            subtypes = self.framework_subtypes_repository.get_framework_subtype_details(subtype_ids)

            return subtypes
        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while fetching subtypes: {e}"
            )
        
    def framework_type_details(self, framework_type_ids: list):
        try:
            # framework_types_repo = FrameworkTypesRepository(session_factory=self.user_selected_answers_repository.session_factory)
            framework_types = self.framework_types_repository.get_framework_type_details(framework_type_ids)

            return framework_types
        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while fetching framework types: {e}"
            )


    # This function saves the user answers in the database
    def save_user_answers(self, user_answers: UserSelectedAnswersBase):
        try:
            
            user_id = user_answers.user_id
            
            # Delete all the previous answer by user just in case to avoid duplication
            self.user_selected_answers_repository.delete_by_user_id(user_id)
            
            # Sending the data to the repository to save the user selected answers
            result = self.user_selected_answers_repository.save_user_answers(user_answers)

            return result

        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while saving selected answers: {e}"
            )

    # This function updates the user answers in the database
    def update_user_answers(self, user_id: int, user_answers: UserSelectedAnswersUpdate):
        try:
            
            # The new answer ids and user id
            answer_ids = user_answers.selected_answers

            # Get all the previously selected user answers
            previous_answers = self.user_selected_answers_repository.get_user_answers(user_id)

            # Get question type of new user selected answers
            question_type = self.get_question_types(answer_ids)

            # IDS of answers to remove
            ids_to_remove = self.get_ids_of_same_question_old_answers(question_type, previous_answers)

            # Delete the previous answers of the user of the same question type
            if len(ids_to_remove) > 0:
                self.del_previous_answers(user_id, ids_to_remove)

            # Sending the data to the repository to save the user selected answers
            result = self.user_selected_answers_repository.update_user_answers(user_id, user_answers)

            return result

        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while updating selected answers: {e}"
            )
            

    # This function updates the user answers in the database
    def update_user_answers_all(self, user_id: int, user_answers: list[QuestionAnswerUpdateDetails]):
        try:
            
            for user_answer in user_answers:
                answer_ids_one_question = user_answer.answer_ids
                self.update_user_answers(user_id, UserSelectedAnswersUpdate(selected_answers=answer_ids_one_question))

            return {
                "status": True,
                "message": f"User answers added successfully."
            }

        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while updating selected answers: {e}"
            )
        

    # This function checks if all the question types are same and then gives their types. Used in update function
    def get_question_types(self, answer_ids: list):
        try:
            answers_repo = AnswersRepository(session_factory=self.user_selected_answers_repository.session_factory)
            question_type = answers_repo.get_question_type_id(answer_ids)

            return question_type
        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while fetching question type of user selected answers: {e}"
            )
        
    # Gets the ids of the questions of the same type as the new answers. Used in update function
    def get_ids_of_same_question_old_answers(self, question_type: int, previous_answers: list):
        try:
            answers_repo = AnswersRepository(session_factory=self.user_selected_answers_repository.session_factory)
            ids = answers_repo.get_ids_of_same_question_old_answers(question_type, previous_answers)

            return ids
        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while filtering out ids to delete: {e}"
            )

    # This function deletes the previous answers of the user of the same question type. Used in update function 
    def del_previous_answers(self, user_id: int, ids_to_remove: list):
        try:
            result = self.user_selected_answers_repository.del_previous_answers(user_id, ids_to_remove)
            return result
        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in user selected answer service while deleting previous answers: {e}"
            )
    
    # This function deletes the previous answers of the user of the same question type
    # def get_user_answers(self, answer_ids: list):
    #     try:
    #         answers_repo = AnswersRepository(session_factory=self.user_selected_answers_repository.session_factory)
    #         question_type = answers_repo.get_question_type_id(answer_ids)

    #         return question_type
    #     except Exception as e:
    #         traceback.print_exc()

    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail= f"Internal Server Error in user selected answer service while fetching question type of user selected answers: {e}"
    #         )
        

        



    # def get_framework_subtypes(self, framework_ids: list):
    #     try:
    #         framework_subtype_repo = FrameworkSubtypesRepository(session_factory=self.question_answer_repository.session_factory)
    #         framework_subtypes = framework_subtype_repo.get_all_framework_subtypes(framework_ids)["framework_subtypes"]

    #         return framework_subtypes
    #     except Exception as e:
    #         traceback.print_exc()

    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail= f"Internal Server Error in question answer service while fetching framework subtypes: {e}"
    #         )
        
    # def get_questions(self, framework_subtype_id: int):
    #     try:
            
    #         questions_repo = QuestionsRepository(session_factory=self.question_answer_repository.session_factory)
    #         questions = questions_repo.get_all_questions(framework_subtype_id)["questions"]

    #         return questions

    #     except Exception as e:
    #         traceback.print_exc()

    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail= f"Internal Server Error in question answer service while fetching questions: {e}"
    #         )
        
    # def get_answers(self, question_id: int):
    #     try:
    #         answers_repo = AnswersRepository(session_factory=self.question_answer_repository.session_factory)
    #         answers = answers_repo.get_all_answers(question_id)["answers"]
    
    #         return answers
    #     except Exception as e:
    #         traceback.print_exc()

    #         raise HTTPException(
    #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #             detail= f"Internal Server Error in question answer service while fetching answers: {e}"
    #         )
    
    
    

