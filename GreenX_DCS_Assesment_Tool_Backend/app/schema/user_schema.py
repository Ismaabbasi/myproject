from typing import List, Optional

from pydantic import BaseModel

from app.schema.base_schema import FindBase, ModelBaseInfo, SearchOptions
from app.util.schema import AllOptional


class BaseUser(BaseModel):
    email: str
    user_token: str
    name: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True

class NewPasswordResponse(BaseUser):
    id: int


class BaseUserWithPassword(BaseUser):
    password: str


class User(ModelBaseInfo, BaseUser, metaclass=AllOptional):
    ...


class FindUser(FindBase, BaseUser, metaclass=AllOptional):
    email: str
    ...


class UpsertUser(BaseUser, metaclass=AllOptional):
    ...


class FindUserResult(BaseModel):
    founds: Optional[List[User]]
    search_options: Optional[SearchOptions]
