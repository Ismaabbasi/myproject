from pydantic import BaseModel, Field
from typing import List, Optional

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    domain_type_id: int

class RoleGet(RoleBase):
    id: int

class GetRolesResponse(BaseModel):
    roles: List[RoleBase]

class Role(RoleBase):
    id: int

    class Config:
        orm_mode: True