from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.user import User
    from app.model.company import Company
    from app.model.domain_types import DomainTypes
    from app.model.roles import Roles

class UserProfile(BaseModel, table=True):
    __tablename__: str = 'user_profiles'
    
    user_id: int = Field(foreign_key='user.id', unique=True, nullable=False)
    company_id: int = Field(foreign_key='company.id', nullable=False)
    domain_id: int = Field(foreign_key='domain_types.id', nullable=False)
    role_id: int = Field(foreign_key='roles.id', nullable=False)

    user: Optional["User"] = Relationship(back_populates="user_profile")
    company: Optional["Company"] = Relationship(back_populates="user_profile")
    domain_type: Optional["DomainTypes"] = Relationship(back_populates="user_profile")
    roles: Optional["Roles"] = Relationship(back_populates="user_profile")
