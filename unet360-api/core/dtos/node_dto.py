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
    minimap: Optional[dict] = Field(
        default=None,
        description="Información del minimapa, ejemplo: {'image': 'ruta.jpg', 'x': 200, 'y': 250}"
    )

class NodeUpdateDTO(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    url_image: Optional[str] = None
    adjacent_nodes: Optional[list[Optional[Dict[str, float]]]] = None
    tags: Optional[Dict[str, list[str]]] = None
    minimap: Optional[dict] = Field(
        default=None,
        description="Información del minimapa, ejemplo: {'image': 'ruta.jpg', 'x': 200, 'y': 250}"
    )

class NodeOutDTO(BaseModel):
    name: str
    location: Optional[str]
    url_image: str
    adjacent_nodes: list[Optional[Dict[str, float]]]
    tags: Dict[str, list[str]]
    minimap: Optional[dict] = Field(
        default=None,
        description="Información del minimapa, ejemplo: {'image': 'ruta.jpg', 'x': 200, 'y': 250}"
    )