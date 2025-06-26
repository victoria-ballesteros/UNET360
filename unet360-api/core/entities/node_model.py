from beanie import Document, Link, Indexed
from pydantic import Field
from typing import List, Optional

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

    location: Optional[Link["Location"]]
    url_image: str
    adyacent_nodes: list[Optional[Link["Node"]]] = Field(
        default = [None, None, None, None],
        description="List of links to adjacent nodes, up to 4 nodes can be linked",
        example=["forward", "backward", "left", "right"]
    )

    tags: Optional[List[Link["Tag"]]]

    class Settings:
        name = "node"
        