from pydantic import BaseModel
from typing import List, Optional


class UserProfileBase(BaseModel):
    user_id: int
    domain_id: int
    role_id: int

class UserProfileCreate(UserProfileBase):
    company_name: str
    
class UserProfileModel(UserProfileBase):
    company_id: int

class UserProfileids(UserProfileBase):
    company_id: int

class GetUserProfileResponse(BaseModel):
    profiles: list[UserProfileids]

class UserProfileUpdate(BaseModel):
    user_id: int
    company_name: Optional[str]
    domain_id: Optional[int]
    role_id: Optional[int]


class UserProfile(UserProfileBase):
    pass

class GetUserProfile(BaseModel):
    class Config:
        orm_mode = True  