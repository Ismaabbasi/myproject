from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.user_selected_measures import UserSelectedMeasures
    from app.model.sustainability_types import SustainabilityTypes
    from app.model.top_of_mind_types import TopOfMindTypes

class SustainabilityMeasures(BaseModel, table=True):
    __tablename__: str = "sustainability_measures"

    name: str = Field(nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    typically_selected: Optional[bool] = Field(default=None, nullable=True)
    sustainability_types_id: Optional[int] = Field(foreign_key="sustainability_types.id", index=True, default=None, nullable=True)
    top_of_mind_types_id: Optional[int] = Field(foreign_key="top_of_mind_types.id", index=True, default=None, nullable=True)

    # Relationships 
    user_selected_measures: List["UserSelectedMeasures"] = Relationship(back_populates="sustainability_measures", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    sustainability_types: Optional["SustainabilityTypes"] = Relationship(back_populates="sustainability_measures")
    top_of_mind_types: Optional["TopOfMindTypes"] = Relationship(back_populates="sustainability_measures")
