from typing import List, Optional, TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Text, Column

from app.model.base_model import BaseModel


if TYPE_CHECKING:
    from app.model.questions import Questions
    from app.model.user_selected_answers import UserSelectedAnswers


class Answers(BaseModel, table=True):
    __tablename__: str = "answers"

    answer: str = Field(
        sa_column=Column(Text)
    )

    questions_id: int = Field(
        foreign_key="questions.id",
        index=True,
        nullable=False
    )

    weight: int = Field(
        default=0,
        index=True
    )

    questions: Optional["Questions"] = Relationship(
        back_populates="answers"
    )

    user_selected_answers: List["UserSelectedAnswers"] = Relationship(
        back_populates="answers",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan"
        }
    )
