from typing import Optional
from pydantic import BaseModel

class DomainBase(BaseModel):
    name: str
    description: Optional[str] = None

class DomainGet(BaseModel):
    id: int
    name: str
    description: str = None

class DomainCreate(BaseModel):
    name: str
    description: Optional[str] = None
    created_by_id: int

class GetDomainResponse(BaseModel):
    domain: list[DomainGet]

class Domain(DomainBase):
    id: int

    class Config:
        orm_mode: True
