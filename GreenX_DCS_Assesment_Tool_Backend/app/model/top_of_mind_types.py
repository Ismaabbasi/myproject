from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.sustainability_measures import SustainabilityMeasures
    from app.model.top_of_mind_roles import TopOfMindRoles

class TopOfMindTypes(BaseModel, table=True):
    __tablename__: str = 'top_of_mind_types'
    
    name: str = Field(unique=True, index=True)
    
    # Relationships
    sustainability_measures: List["SustainabilityMeasures"] = Relationship(back_populates="top_of_mind_types", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    top_of_mind_roles: List["TopOfMindRoles"] = Relationship(back_populates="top_of_mind_types", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
