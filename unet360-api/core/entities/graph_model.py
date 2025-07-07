from pydantic import BaseModel
from typing import Dict, List

class GraphNode(BaseModel):
    name: str
    adjacent_nodes: Dict[str, float]  # {node_name: weight}

class GraphPath(BaseModel):
    nodes: List[str]
    total_weight: float