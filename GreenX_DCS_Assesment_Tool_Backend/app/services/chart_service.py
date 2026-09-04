from sqlalchemy.orm import Session
from app.repository import FrameworkTypesRepository, QuestionsRepository, AnswersRepository, UserSelectedAnswersRepository

from app.schema.chart_schema import SpiderChartGet

from app.services.base_service import is_valid_name, is_valid_description
from fastapi import HTTPException, status
import traceback

import logging

leaders_maturity_level = [
    [4, 4, 4, 5, 4, 3], # Strategy
    [4, 5, 4, 3], # Governance
    [3, 4, 5, 5], # Execution
    [4, 5, 4, 4, 4, 3, 5], # IT for Sustainable Business
    [4, 3, 4, 5, 4, 4, 3, 4, 4, 4, 4, 5, 3, 3], # Sustainable IT
    [5, 4, 4] # ESG
]


class ChartService:
    def __init__(self, framework_types_repository: FrameworkTypesRepository, questions_repository: QuestionsRepository, answers_repository: AnswersRepository, user_selected_answers_repository: UserSelectedAnswersRepository):
        self.framework_types_repository = framework_types_repository
        self.questions_repository = questions_repository
        self.answers_repository = answers_repository
        self.user_selected_answers_repository = user_selected_answers_repository
        
    def calc_scoring_threshold_subtype(self, total_weightage: int, user_weightage: int):
        # Level 1: 0-20% of the total weightage
        # Level 2: 21-40% of the total weightage
        # Level 3: 41-60% of the total weightage
        # Level 4: 61-80% of the total weightage
        # Level 5: 81-100% of the total weightage
        
        # Total weightage of subtype risk = 10 
        # User selected answer weightage = 7
        # 
        
        if user_weightage <= total_weightage * 0.2:
            return 1
        elif user_weightage <= total_weightage * 0.4:
            return 2
        elif user_weightage <= total_weightage * 0.6:
            return 3
        elif user_weightage <= total_weightage * 0.8:
            return 4
        else:
            return 5
        
        
        
    
    def get_spider_chart(self, chart_data: SpiderChartGet):
        pass
        
        # Framework id
        framework_id = chart_data.framework_id
        
        # First, get the framework name from the chart data and all of its subtype names.
        framework_data = self.framework_types_repository.get_framework_data_spider_chart(framework_id)
        
        # Framework name
        framework_name = framework_data.name if framework_data else ""
        
        # Framework subtypes name along with their ids
        subtypes = []
        if framework_data:
            for subtype in framework_data.framework_subtype:
                subtypes.append({
                    "id": subtype.id,
                    "name": subtype.name
                })
                 
        # Now we will calculate user maturity level from 1-5 for each subtype according to the answers the user choose
        user_maturity_level = []
        
        # User id
        user_id = chart_data.user_id
        
        # The logic to calculate the user maturity level for each subtype will be as follows:
        # Each question has a maximum of level of 5 weightage. So, the total or maximum weightage for each question will be total questions * 5.
        # The user maturity level will be calculated as follows:
        # Each has a weightage point from 0-5. So, the user maturity level will be calculated as follows:
        # As we have to determine the maturity level overall for each subtype, we will calculate as per the following formula.
        # Level 1: 0-20% of the total weightage
        # Level 2: 21-40% of the total weightage
        # Level 3: 41-60% of the total weightage
        # Level 4: 61-80% of the total weightage
        # Level 5: 81-100% of the total weightage
        
        total_weightages = []
        user_maturity_level = []
        
        # Calculate the user maturity level for each subtype
        for subtype in subtypes:
            pass
            # Get all the questions for the subtype and then we will calculate the total weightage for each subtype.
            questions = self.questions_repository.get_questions_subtype_id(subtype["id"])
            
            if questions != {}:
                # Total weightage for current user type
                total_weightage = len(questions) * 5
                total_weightages.append(total_weightage)
                
                # Get all the possible answer ids for the questions of the current subtype
                question_ids = [question.id for question in questions]
                
                answers = self.answers_repository.get_all_answers(question_ids)["answers"]
                
                # Get all the answers of the question of the current subtype
                answer_ids = [answer.id for answer in answers]
                
                # Get all the answers user has selected for the current subtype
                user_answer_ids = self.user_selected_answers_repository.get_user_answers_subtype(user_id, answer_ids)
                
                # Now we have all the answer user has selected for the questions in the subtype. Now we will add up the weightage of the answers to get the user maturity level for the current subtype.
                total_user_subtype_answer_weightage = 0
                for answer in answers:
                    if answer.id in user_answer_ids:
                        total_user_subtype_answer_weightage += answer.weight
        
                # Calculate the user maturity level for the current subtype
                result = self.calc_scoring_threshold_subtype(total_weightage, total_user_subtype_answer_weightage)
                
                # Add the result to the user maturity level list
                user_maturity_level.append(result)
            
            
        return {
            "framework_name": framework_name,
            "subtypes": subtypes,
            "leaders_maturity_level": leaders_maturity_level[framework_id - 1] if len(leaders_maturity_level) >= framework_id else [],
            "user_maturity_level": user_maturity_level
        }
        
        

    
    

