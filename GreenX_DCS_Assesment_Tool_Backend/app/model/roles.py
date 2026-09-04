from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.domain_types import DomainTypes
    from app.model.user_profile import UserProfile
    from app.model.top_of_mind_roles import TopOfMindRoles

class Roles(BaseModel, table=True):
    __tablename__: str = 'roles'

    domain_type_id: int = Field(foreign_key="domain_types.id", index=True, nullable=False)
    name: str = Field(unique=True, nullable=False)

    domain_type: Optional["DomainTypes"] = Relationship(back_populates="roles")
    user_profile: List["UserProfile"] = Relationship(back_populates="roles", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    top_of_mind_roles: List["TopOfMindRoles"] = Relationship(back_populates="roles", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
