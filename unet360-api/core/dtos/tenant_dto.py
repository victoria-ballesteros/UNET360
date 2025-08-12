from pydantic import BaseModel
from typing import Optional, Literal

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

class TenantStatusDTO(BaseModel):
    name: str
    status: Literal["OK", "WARNING", "ERROR"]