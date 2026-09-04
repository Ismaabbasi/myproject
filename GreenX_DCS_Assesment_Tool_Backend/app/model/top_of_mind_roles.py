from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.top_of_mind_types import TopOfMindTypes
    from app.model.roles import Roles

class TopOfMindRoles(BaseModel, table=True):
    __tablename__: str = 'top_of_mind_roles'
    
    top_of_mind_types_id: Optional[int] = Field(foreign_key="top_of_mind_types.id", index=True, nullable=True)
    role_id: Optional[int] = Field(foreign_key="roles.id", index=True, nullable=True)
    
    # Relationships
    top_of_mind_types: Optional["TopOfMindTypes"] = Relationship(back_populates="top_of_mind_roles")
    roles: Optional["Roles"] = Relationship(back_populates="top_of_mind_roles")
