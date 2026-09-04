from pydantic import BaseModel, Field
from typing import List, Optional

class UserSelectedAnswersBase(BaseModel):
  user_id: int
  selected_answers: List[int]

class UserSelectedAnswersUpdate(BaseModel):
  selected_answers: List[int]
  
class QuestionAnswerUpdateDetails(BaseModel):
  question_id: int
  answer_ids: List[int]
  
class UserSelectedAnswersUpdateAll(BaseModel):
  selected_answers: List[QuestionAnswerUpdateDetails]

# class UserMeasuresCreate(UserSelectedAnswersBase):
#     pass
#     sustainability_types_id: int
#     new_measure: Optional[str] = None

# class UserMeasuresData(BaseModel):
#     id: int
#     measure: str
#     info: str

# class GetUserSelectedMeasuresData(BaseModel):
#     user_id: int
#     sustainability_measures_type_id: int

# class GetUserMeasuresResponse(BaseModel):
#     measures: List[UserMeasuresData]

# class GetUserMeasuresByDomainIdResponse(BaseModel):
#     domain_id: int
#     role_id: int


class Role(UserSelectedAnswersBase):
    id: int

    class Config:
        orm_mode: True