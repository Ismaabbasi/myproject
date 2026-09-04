from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.user import User
    from app.model.sustainability_measures import SustainabilityMeasures

class UserSelectedMeasures(BaseModel, table=True):
    __tablename__: str = 'user_selected_measures'
    
    sustainability_measures_id: int = Field(foreign_key='sustainability_measures.id', index=True, nullable=False)
    user_id: int = Field(foreign_key='user.id', index=True, nullable=False)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="user_selected_measures")
    sustainability_measures: Optional["SustainabilityMeasures"] = Relationship(back_populates="user_selected_measures")
