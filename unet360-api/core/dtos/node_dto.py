from pydantic import BaseModel, Field
from typing import Optional, List

class NodeCreateDTO(BaseModel):
    name: str
    location: Optional[str] = None
    url_image: str
    adyacent_nodes: List[Optional[str]] = Field(
        default_factory=lambda: [None, None, None, None],
        description="List of up to 4 adjacent node names (forward, back, left, right)"
    )
    tags: Optional[list[str]] = Field(default_factory=list)

class NodeUpdateDTO(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    url_image: Optional[str] = None
    adyacent_nodes: Optional[List[Optional[str]]] = None
    tags: Optional[List[str]] = None

class NodeOutDTO(BaseModel):
    name: str
    location: Optional[str]
    url_image: str
    adyacent_nodes: List[Optional[str]]
    tags: List[str]