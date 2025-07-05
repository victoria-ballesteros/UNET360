from pydantic import BaseModel, Field
from typing import Optional

class NodeCreateDTO(BaseModel):
    name: str
    location: Optional[str] = None
    url_image: str
    adyacent_nodes: list[Optional[str]] = Field(
        default_factory=lambda: [None, None, None, None],
        description="list of up to 4 adjacent node names (forward, back, left, right)"
    )
    tags: Optional[list[str]] = Field(default_factory=list)

class NodeUpdateDTO(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    url_image: Optional[str] = None
    adyacent_nodes: Optional[list[Optional[str]]] = None
    tags: Optional[list[str]] = None

class NodeOutDTO(BaseModel):
    name: str
    location: Optional[str]
    url_image: str
    adyacent_nodes: list[Optional[str]]
    tags: list[str]