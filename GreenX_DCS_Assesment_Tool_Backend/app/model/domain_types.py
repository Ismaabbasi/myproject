from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.roles import Roles
    from app.model.user_profile import UserProfile
    from app.model.user import User
    

class DomainTypes(BaseModel, table=True):
    __tablename__: str = 'domain_types'
    
    name: str = Field(unique=True, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    created_by_id: Optional[int] = Field(foreign_key="user.id", nullable=True)
    
    # Relationships
    user: Optional["User"] = Relationship(back_populates="domain_types")
    roles: List["Roles"] = Relationship(back_populates="domain_type", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    user_profile: List["UserProfile"] = Relationship(back_populates="domain_type", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
