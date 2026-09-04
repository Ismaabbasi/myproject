from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.user_profile import UserProfile

class Company(BaseModel, table=True):
    __tablename__: str = 'company'
    
    name: str = Field(index=True, nullable=False)

    user_profile: List["UserProfile"] = Relationship(back_populates="company", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
