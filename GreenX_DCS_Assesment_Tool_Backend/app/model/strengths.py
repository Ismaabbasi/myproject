from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.user import User

class Strengths(BaseModel, table=True):
    __tablename__: str = 'strengths'
    
    user_id: int = Field(foreign_key="user.id", nullable=False)
    strength: str = Field(nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="strengths")
