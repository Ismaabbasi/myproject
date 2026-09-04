from pydantic import BaseModel, Field
from typing import List, Optional

class UserMeasuresBase(BaseModel):
  user_id: int
  measures: List[int]

class UserMeasuresCreate(UserMeasuresBase):
    pass
    sustainability_types_id: int
    new_measure: Optional[str] = None
    
class OtherMeasuresCreate(BaseModel):
    user_id: int
    sustainability_types_id: int
    other_measure: str

class UserMeasuresData(BaseModel):
    id: int
    measure: str
    info: str

class GetUserSelectedMeasuresData(BaseModel):
    user_id: int
    sustainability_measures_type_id: int

class GetUserMeasuresResponse(BaseModel):
    measures: List[UserMeasuresData]

class GetUserMeasuresByDomainIdResponse(BaseModel):
    domain_id: int
    role_id: int


class Role(UserMeasuresBase):
    id: int

    class Config:
        orm_mode: True