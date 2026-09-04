from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.sustainability_measures import SustainabilityMeasures
    from app.model.other_measures import OtherMeasures

class SustainabilityTypes(BaseModel, table=True):
    __tablename__: str = 'sustainability_types'
    
    name: str = Field(unique=True, nullable=False)
    
    # Relationships
    sustainability_measures: List["SustainabilityMeasures"] = Relationship(back_populates="sustainability_types", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    other_measures: List["OtherMeasures"] = Relationship(back_populates="sustainability_types", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
