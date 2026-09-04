from pydantic import BaseModel, Field
from typing import List, Optional

class SpiderChartGet(BaseModel):
    user_id: int
    framework_id: int

# class ResetPassword(BaseModel):
#     email: str
#     password: str
#     password_repeat: str

# class OtpCreate(OtpBase):
#     pass

# class Role(OtpBase):
#     id: int

#     class Config:
#         orm_mode: True