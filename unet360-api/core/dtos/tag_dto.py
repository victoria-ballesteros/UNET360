from pydantic import BaseModel
from typing import Optional

class TagCreateDTO(BaseModel):
    name: str
    icon_name: Optional[str]

class TagUpdateDTO(BaseModel):
    name: Optional[str]
    icon_name: Optional[str]

class TagOutDTO(BaseModel):
    name: str
    icon_name: Optional[str]
