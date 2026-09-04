from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.framework_subtypes import FrameworkSubtypes
    from app.model.answers import Answers
    from app.model.comment import Comment

class Questions(BaseModel, table=True):
    __tablename__: str = 'questions'
    
    question: str = Field(nullable=False)
    is_single_choice: Optional[bool] = Field(default=True)
    framework_subtypes_id: int = Field(foreign_key="framework_subtypes.id", index=True, nullable=False)
    
    framework_subtype: Optional["FrameworkSubtypes"] = Relationship(back_populates="questions")
    answers: List["Answers"] = Relationship(back_populates="questions", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    comment: List["Comment"] = Relationship(back_populates="questions", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
