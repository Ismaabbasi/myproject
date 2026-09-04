from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.framework_subtypes import FrameworkSubtypes

class FrameworkTypes(BaseModel, table=True):
    __tablename__: str = 'framework_types'
    
    name: str = Field(unique=True, nullable=False)

    framework_subtype: List["FrameworkSubtypes"] = Relationship(back_populates="framework_type", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
