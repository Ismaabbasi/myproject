from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.sustainability_types import SustainabilityTypes
    from app.model.user import User

class OtherMeasures(BaseModel, table=True):
    __tablename__: str = "other_measures"

    user_id: int = Field(foreign_key="user.id", index=True, nullable=False)
    sustainability_types_id: int = Field(foreign_key="sustainability_types.id", index=True, nullable=False)
    other_measure: str = Field(nullable=False, max_length=2000)

    # Relationships 
    user: Optional["User"] = Relationship(back_populates="other_measures")
    sustainability_types: Optional["SustainabilityTypes"] = Relationship(back_populates="other_measures")
