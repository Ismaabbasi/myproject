from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.otp_password import OtpPassword
    from app.model.user_profile import UserProfile
    from app.model.user_selected_measures import UserSelectedMeasures
    from app.model.user_selected_answers import UserSelectedAnswers
    from app.model.comment import Comment
    from app.model.domain_types import DomainTypes
    from app.model.other_measures import OtherMeasures
    from app.model.strengths import Strengths
    from app.model.improvements import Improvements
    

class User(BaseModel, table=True):
    __tablename__: str = "user"

    email: str = Field(unique=True, index=True)
    password: str = Field()
    user_token: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None, nullable=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    
    # Relationships
    otp_password: List["OtpPassword"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    user_profile: List["UserProfile"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    user_selected_measures: List["UserSelectedMeasures"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    user_selected_answers: List["UserSelectedAnswers"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    comment: List["Comment"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    domain_types: List["DomainTypes"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    other_measures: List["OtherMeasures"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    strengths: List["Strengths"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    improvements: List["Improvements"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})