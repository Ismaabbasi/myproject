from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# class MeasuresBase(BaseModel):
#     name: str
#     sustainability_types_id: int

class GetSubtypeQuestionAnswers(BaseModel):
    user_id: int
    subtype_id: int

# class MeasuresData(BaseModel):
#     id: int
#     name: str

# class TypicallySelectedMeasures(BaseModel):
#     id: int
#     name: str
#     description: str = None

# class GetMeasuresResponse(BaseModel):
#     measures: List[MeasuresData]
#     typically_selected_measures: List[TypicallySelectedMeasures]

# class GetMeasuresByDomainIdResponse(BaseModel):
#     sustainability_types_id: int
#     role_id: Optional[int]


# class Role(MeasuresBase):
#     id: int

#     class Config:
#         orm_mode: True