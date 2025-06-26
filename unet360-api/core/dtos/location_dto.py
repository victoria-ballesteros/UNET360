from pydantic import BaseModel
from typing import Optional


class LocationCreateDTO(BaseModel):
    name: str


class LocationUpdateDTO(BaseModel):
    name: Optional[str]


class LocationOutDTO(BaseModel):
    name: str
