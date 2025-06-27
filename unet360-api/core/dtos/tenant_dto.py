from pydantic import BaseModel
from typing import Optional

class TenantCreateDTO(BaseModel):
    name: str
    supabase_user_id: str
    role: str

class TenantUpdateDTO(BaseModel):
    name: Optional[str]
    role: Optional[str]

class TenantOutDTO(BaseModel):
    name: str
    role: str