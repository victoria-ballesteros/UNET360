from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Literal
import math

class NodeCreateDTO(BaseModel):
    name: str
    location: Optional[str] = None
    url_image: str
    adjacent_nodes: list[Optional[Dict[str, float]]] = Field(
        default_factory=lambda: [None, None, None, None],
        description="list of up to 4 adjacent node names (forward, back, left, right)"
    )
    arrow_angles: List[Optional[float]] = Field(
        default_factory=lambda: [0, math.pi / 2, math.pi, -math.pi / 2],
        description="Angles to position arrows on the 360 image; allow nulls for missing arrows"
    )
    forward_heading: float = Field(default=0.0, description="Heading (radians) of the image front")
    tags: Optional[Dict[str, Dict[str, float]]] = Field(
        default_factory=dict,
        description="Dictionary of tags with per-value heading"
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
    arrow_angles: Optional[List[Optional[float]]] = None
    forward_heading: Optional[float] = None
    tags: Optional[Dict[str, Dict[str, float]]] = None
    minimap: Optional[dict] = Field(
        default=None,
        description="Información del minimapa, ejemplo: {'image': 'ruta.jpg', 'x': 200, 'y': 250}"
    )

class NodeOutDTO(BaseModel):
    name: str
    location: Optional[str]
    url_image: str
    adjacent_nodes: list[Optional[Dict[str, float]]]
    # New fields
    arrow_angles: List[Optional[float]]
    forward_heading: float
    tags: Dict[str, Dict[str, float]]
    minimap: Optional[dict] = Field(
        default=None,
        description="Información del minimapa, ejemplo: {'image': 'ruta.jpg', 'x': 200, 'y': 250}"
    )


class NodeStatusDTO(BaseModel):
    name: str
    status: Literal["OK", "WARNING", "ERROR"]
    reasons: Optional[List[str]] = None
