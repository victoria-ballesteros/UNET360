from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from core.entities.graph_model import GraphNode, GraphPath

class GraphServicePort(ABC):
    @abstractmethod
    async def get_shortest_path(self, source: str, target: str) -> Optional[GraphPath]:
        pass
    
    @abstractmethod
    async def refresh_graph(self) -> None:
        pass
    
    @abstractmethod
    async def get_all_nodes(self) -> List[GraphNode]:
        pass
    
    @abstractmethod
    async def get_adjacent_nodes(self, node_name: str) -> Dict[str, float]:
        pass