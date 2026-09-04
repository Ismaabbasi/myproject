from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.answers import Answers
    from app.model.user import User

class UserSelectedAnswers(BaseModel, table=True):
    __tablename__: str = 'user_selected_answers'
    
    answer_id: int = Field(foreign_key='answers.id', index=True, nullable=False)
    user_id: int = Field(foreign_key='user.id', index=True, nullable=False)

    answers: Optional["Answers"] = Relationship(back_populates="user_selected_answers")
    user: Optional["User"] = Relationship(back_populates="user_selected_answers")
