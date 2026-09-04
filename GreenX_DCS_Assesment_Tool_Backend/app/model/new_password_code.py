from sqlmodel import Field, SQLModel
from typing import Optional, TYPE_CHECKING
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.user import User

class NewPasswordCode(BaseModel, table=True):
    __tablename__: str = 'new_password_code'
    
    code: str = Field(unique=True, nullable=False)
    user_id: Optional[int] = Field(foreign_key="user.id", index=True, nullable=False)
    
    # Uncomment if there's a relationship with User
    # user: Optional["User"] = Relationship(back_populates="new_password_code")
