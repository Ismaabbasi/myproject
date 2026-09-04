from sqlmodel import Field, SQLModel
from typing import Optional
from app.model.base_model import BaseModel

class TokenBlacklist(BaseModel, table=True):
    __tablename__: str = "token_blacklist"

    access_token: str = Field(index=True, unique=True, nullable=False)
