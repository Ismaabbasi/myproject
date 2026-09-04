from sqlalchemy.orm import Session

from app.repository.question_answer_repository import QuestionAnswerRepository
from app.repository.framework_types_repository import FrameworkTypesRepository
from app.repository.framework_subtypes_repository import FrameworkSubtypesRepository
from app.repository.questions_repository import QuestionsRepository
from app.repository.answers_repository import AnswersRepository
from app.repository.user_selected_answers_repository import UserSelectedAnswersRepository
from app.repository.comment_repository import CommentRepository
from app.schema.question_answer_schema import GetSubtypeQuestionAnswers
from app.services.base_service import is_valid_name, is_valid_description
from fastapi import HTTPException, status
import traceback

class QuestionAnswerService:
    def __init__(self, question_answer_repository: QuestionAnswerRepository, framework_types_repository: FrameworkTypesRepository, framework_subtypes_repository: FrameworkSubtypesRepository, questions_repository: QuestionsRepository, answers_repository: AnswersRepository, user_selected_answers_repository: UserSelectedAnswersRepository, comment_repository: CommentRepository):
        self.framework_types_repository = framework_types_repository
        self.framework_subtypes_repository = framework_subtypes_repository
        self.questions_repository = questions_repository
        self.answers_repository = answers_repository
        self.question_answer_repository = question_answer_repository
        self.user_selected_answers_repository = user_selected_answers_repository
        self.comment_repository = comment_repository

    # This function will give all the questions and their possible options when a subtype id is given
    def get_questions_answers_subtype(self, subtype_data: GetSubtypeQuestionAnswers):
        try:
            subtype_id = subtype_data.subtype_id
            user_id = subtype_data.user_id
            
            # Get the framework and framework subtype name through subtype id
            subtype_details = self.framework_subtypes_repository.get_framework_subtype_details([subtype_id])
            framework_name = ""
            framework_subtype_name = ""
            
            if len(subtype_details) > 0:
                subtype_details = subtype_details[0]
                framework_subtype_name = subtype_details["name"]
                # Getting the framework type name
                framework_details = self.framework_types_repository.get_framework_type_details([subtype_details["framework_type_id"]])
                
                if len(framework_details) > 0:
                    framework_details = framework_details[0]
                    framework_name = framework_details["name"]
            
            # Getting the questions of the subtype
            subtype_id_list = []
            subtype_id_list.append(subtype_id)
            questions = self.get_questions(subtype_id_list)

            # Store questions ids in a list
            question_ids = []
            for question in questions:
                question_ids.append(question.id)

            # Getting the answers of the questions
            answers = self.get_answers(question_ids)
            
            # Getting the answer ids selected by the user
            user_answers_ids = self.user_selected_answers_repository.get_user_answers(user_id)
            
            # Getting the comments for these questions if any
            comments = self.comment_repository.get_comments_by_user(user_id)

            # # Adding the questions and answers to the response
            response = []
            
            for question in questions:
                
                comment_text = ""
                
                for comment in comments:
                    if comment.question_id == question.id:
                        comment_text = comment.comment
                        break
                
                question_dict = {
                    "question_id": question.id,
                    "question": question.question,
                    "is_single_choice": question.is_single_choice,
                    "comment": comment_text,
                    "answer_values": []
                }

                for answer in answers:
                    if question.id == answer.questions_id:
                        answer_dict = {
                            "answer_id": answer.id,
                            "answer": answer.answer,
                            "is_selected": answer.id in user_answers_ids
                        }

                        question_dict["answer_values"].append(answer_dict)

                response.append(question_dict)

            return {
                "framework_name": framework_name,
                "subtype_name": framework_subtype_name,
                "questions": response
            }
            # return question_ids

        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in question answer service while fetching questions and answers of subtype: {e}"
            )

    def get_all_question_answer(self):
        try:
            framework_types = self.get_framework_types()
            
            # These will be the overall response containing everything
            response = []

            # Adding the framework types (name and id) to the response. 
            # The subtypes_values will hold the subtypes of the framework type and their respective questions and answers.
            for framework_type in framework_types:
                type_dict = {
                    "framework_id": framework_type.id,
                    "framework_name": framework_type.name,
                    "subtypes_values": []
                }

                response.append(type_dict)

            # Getting the framework type ids to get the subtypes of the framework types
            framework_type_ids = []
            for framework_type in framework_types:
                framework_type_ids.append(framework_type.id)

            # Getting the subtypes of the framework types. (id, name, framework_type_id)
            framework_subtypes = self.get_framework_subtypes(framework_type_ids)

            # Adding the subtypes to the response in the subtypes_values which was empty previously.
            # The question_values will hold the questions and answers.
            for framework_type in response:
                for framework_subtype in framework_subtypes:
                    if framework_type["framework_id"] == framework_subtype.framework_type_id:
                        subtype_dict = {
                            "subtype_id": framework_subtype.id,
                            "subtype_name": framework_subtype.name,
                            "question_values": []
                        }

                        framework_type["subtypes_values"].append(subtype_dict)

            
            # Now we will get the questions of the subtypes

            # Getting the framework subtype ids to get the questions of the subtypes
            framework_subtype_ids = []
            for framework_subtype in framework_subtypes:
                framework_subtype_ids.append(framework_subtype.id)

            # Getting the questions of the subtypes. (id, framework_subtype_id, question)
            questions = self.get_questions(framework_subtype_ids)

            # keeping count of questions
            question_count = 0

            # Adding the questions to the response in the question_values which was empty previously.
            # The answer_values will hold the answers.
            for framework_type in response:
                for framework_subtype in framework_type["subtypes_values"]:
                    for question in questions:
                        if framework_subtype["subtype_id"] == question.framework_subtypes_id:
                            question_dict = {
                                "question_id": question.id,
                                "question": question.question,
                                "is_single_choice": question.is_single_choice,
                                "answer_values": []
                            }

                            framework_subtype["question_values"].append(question_dict)

                            question_count += 1


            # Now we will get the answers of the questions
            # Getting the question ids to get the answers of the questions
            question_ids = []
            for question in questions:
                question_ids.append(question.id)

            # Getting the answers of the questions. (id, questions_id, answer)
            answers = self.get_answers(question_ids)

            # Adding the answers to the response in the answer_values which was empty previously.
            for framework_type in response:
                for framework_subtype in framework_type["subtypes_values"]:
                    for question in framework_subtype["question_values"]:
                        for answer in answers:
                            if question["question_id"] == answer.questions_id:
                                answer_dict = {
                                    "answer_id": answer.id,
                                    "answer": answer.answer
                                }

                                question["answer_values"].append(answer_dict)


            result = {
                "total_questions": question_count,
                "question_answer": response
            }


            return result

        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in question answer service while fetching all types, subtypes, questions and answers: {e}"
            )


    def get_framework_types(self):
        try:
            framework_types = self.framework_types_repository.get_all_framework_types()["framework_types"]

            return framework_types
        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in question answer service while fetching framework types: {e}"
            )


    def get_framework_subtypes(self, framework_ids: list):
        try:
            framework_subtypes = self.framework_subtypes_repository.get_all_framework_subtypes(framework_ids)["framework_subtypes"]

            return framework_subtypes
        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in question answer service while fetching framework subtypes: {e}"
            )
        
    def get_questions(self, framework_subtype_id: list):
        try:
            questions = self.questions_repository.get_all_questions(framework_subtype_id)["questions"]

            return questions

        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in question answer service while fetching questions: {e}"
            )
        
    def get_answers(self, question_id: list):
        try:
            answers = self.answers_repository.get_all_answers(question_id)["answers"]
    
            return answers
        except Exception as e:
            traceback.print_exc()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= f"Internal Server Error in question answer service while fetching answers: {e}"
            )
    
    
    

