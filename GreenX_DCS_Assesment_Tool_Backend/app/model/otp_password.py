from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from app.model.base_model import BaseModel

if TYPE_CHECKING:
    from app.model.user import User

class OtpPassword(BaseModel, table=True):
    __tablename__: str = 'otp_password'
    
    user_email: str = Field(foreign_key="user.email", index=True, unique=True, nullable=False)
    code: str = Field(unique=True, nullable=False)
    expiration_date: datetime = Field(nullable=False)
    
    user: Optional["User"] = Relationship(back_populates="otp_password")
