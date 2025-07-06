from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class NodeCreateDTO(BaseModel):
    name: str
    location: Optional[str] = None
    url_image: str
    adjacent_nodes: list[Optional[Dict[str, float]]] = Field(
        default_factory=lambda: [None, None, None, None],
        description="list of up to 4 adjacent node names (forward, back, left, right)"
    )
    tags: Optional[Dict[str, list[str]]] = Field(
        default_factory=dict,
        description="Dictionary of tags with values"
    )

class NodeUpdateDTO(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    url_image: Optional[str] = None
    adjacent_nodes: Optional[list[Optional[Dict[str, float]]]] = None
    tags: Optional[Dict[str, list[str]]] = None

class NodeOutDTO(BaseModel):
    name: str
    location: Optional[str]
    url_image: str
    adjacent_nodes: list[Optional[Dict[str, float]]]
    tags: Dict[str, list[str]]