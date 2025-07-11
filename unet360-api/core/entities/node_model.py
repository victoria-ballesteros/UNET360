from beanie import Document, Link, Indexed
from pydantic import Field
from typing import Optional, Dict, List

from .location_model import Location
from .tag_model import Tag

class Node(Document):
    name: Indexed(str, unique=True) = Field(
        ...,
        min_length=3,
        max_length=30,
        description="Unique name of the node, Starting with a number (e.g., 002, 043, 583), optionally followed by a name.",
        example="003-HallA",
        pattern=r"^\d+(-[a-zA-Z0-9]+)*$"
    )
    location: Optional[Link[Location]]
    url_image: str

    adjacent_nodes: List[Optional[Dict[str, float]]] = Field(
        default=[None, None, None, None],
        description="Lista de 4 posiciones [frente, atrás, izquierda, derecha] con {node_id: peso}",
        example=[{"003": 1.5}, None, {"001": 0.5}, None]
    )
    
    tags: Optional[Dict[str, List[str]]] = Field(
        description="Clave = nombre del tag, Valores = lista"
    )

    class Settings:
        name = "node"
        