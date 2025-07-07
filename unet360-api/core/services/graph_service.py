from typing import Optional, List, Dict
from core.ports.graph_service_port import GraphServicePort
from core.entities.graph_model import GraphPath, GraphNode
from core.exceptions.graph_exceptions import NodeNotFoundError, NoPathError

class GraphService:
    def __init__(self, graph_adapter: GraphServicePort):
        self.graph_adapter = graph_adapter
    
    async def calculate_shortest_path(self, source: str, target: str) -> GraphPath:
        path = await self.graph_adapter.get_shortest_path(source, target)
        if not path:
            if source not in [node.name for node in await self.graph_adapter.get_all_nodes()]:
                raise NodeNotFoundError(source)
            if target not in [node.name for node in await self.graph_adapter.get_all_nodes()]:
                raise NodeNotFoundError(target)
            raise NoPathError(source, target)
        return path
    
    async def refresh_graph(self) -> None:
        await self.graph_adapter.refresh_graph()
    
    async def get_all_nodes(self) -> List[GraphNode]:
        return await self.graph_adapter.get_all_nodes()
    
    async def get_adjacent_nodes(self, node_name: str) -> Dict[str, float]:
        adjacent = await self.graph_adapter.get_adjacent_nodes(node_name)
        if not adjacent and node_name not in [node.name for node in await self.graph_adapter.get_all_nodes()]:
            raise NodeNotFoundError(node_name)
        return adjacent