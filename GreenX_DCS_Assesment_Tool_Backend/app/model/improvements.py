from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.user import User

class Improvements(BaseModel, table=True):
    __tablename__: str = 'improvements'
    
    user_id: int = Field(foreign_key="user.id", nullable=False)
    improvement: str = Field(nullable=False)

    # Relationships
    user: "User" = Relationship(back_populates="improvements")
