from datetime import datetime

from pydantic import BaseModel

from app.schema.user_schema import User


class SignIn(BaseModel):
    email: str
    password: str


class SignUp(BaseModel):
    email: str
    password: str
    name: str


class Payload(BaseModel):
    id: int
    email: str
    name: str
    is_superuser: bool


class SignInResponse(BaseModel):
    access_token: str
    expiration: datetime
    user_info: User
    group_id: int
    role_id: int
    role: str
    has_profile: bool
    has_top_of_mind: bool
    has_value_drivers: bool
    has_main_challenges: bool


