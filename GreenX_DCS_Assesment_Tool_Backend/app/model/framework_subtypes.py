from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.framework_types import FrameworkTypes
    from app.model.questions import Questions

class FrameworkSubtypes(BaseModel, table=True):
    __tablename__: str = 'framework_subtypes'
    
    name: str = Field(nullable=False)
    framework_type_id: int = Field(foreign_key='framework_types.id', index=True, nullable=False)

    framework_type: Optional["FrameworkTypes"] = Relationship(back_populates="framework_subtype")
    questions: List["Questions"] = Relationship(back_populates="framework_subtype", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
