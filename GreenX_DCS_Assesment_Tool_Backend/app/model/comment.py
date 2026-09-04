from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.questions import Questions
    from app.model.user import User

class Comment(BaseModel, table=True):
    __tablename__: str = 'comment'
    
    comment: str = Field(index=True, nullable=False)
    question_id: int = Field(foreign_key="questions.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)

    # Relationships
    questions: "Questions" = Relationship(back_populates="comment")
    user: "User" = Relationship(back_populates="comment")
