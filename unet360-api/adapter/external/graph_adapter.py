import networkx as nx
from typing import Dict, List, Optional
from core.ports.graph_service_port import GraphServicePort
from core.entities.graph_model import GraphNode, GraphPath
from adapter.database.node_repository import NodeRepository

class NetworkXGraphService(GraphServicePort):
    """Adaptador de servicio de grafo utilizando NetworkX para manejar nodos y caminos."""
    _instance = None
    
    def __new__(cls, node_repository: NodeRepository):
        """Implementación del patrón para asegurar una única instancia."""
        if cls._instance is None:
            cls._instance = super(NetworkXGraphService, cls).__new__(cls)
            cls._instance.graph = nx.Graph()
            cls._instance.node_repository = node_repository
        return cls._instance
    
    async def _convert_to_graph_node(self, node) -> GraphNode:
        """Convierte un nodo de la base de datos a un GraphNode."""
        adjacent_nodes = {}
        for adj in node.adjacent_nodes:
            if adj is not None:
                adj_name = next(iter(adj.keys()))
                weight = adj[adj_name]
                adjacent_nodes[adj_name] = weight
        return GraphNode(name=node.name, adjacent_nodes=adjacent_nodes)
    
    async def refresh_graph(self) -> None:
        """Refresca el grafo cargando aristas solo si hay adyacencia recíproca con igual peso.

        - Carga los nodos desde BD.
        - Construye aristas únicamente cuando A->B y B->A existen y el peso coincide.
        - Excluye del grafo los nodos que no participan en ninguna arista válida.
        """
        db_nodes = await self.node_repository.get_all()
        self.graph.clear()

        # Índice para consultas rápidas
        name_to_node = {n.name: n for n in db_nodes}

        # Recolectar aristas válidas (evitar duplicados con ordenación de extremos)
        valid_edges: set[tuple[str, str, float]] = set()

        for node in db_nodes:
            # Cada entrada de adjacent_nodes puede ser None o un dict {name: weight}
            for adj in (getattr(node, 'adjacent_nodes', None) or []):
                if not isinstance(adj, dict) or len(adj) != 1:
                    continue
                (neighbor_name, weight), = adj.items()
                if neighbor_name not in name_to_node:
                    continue
                # Validar reciprocity con igual peso
                neighbor = name_to_node[neighbor_name]
                reciprocal_ok = False
                for back in (getattr(neighbor, 'adjacent_nodes', None) or []):
                    if isinstance(back, dict) and node.name in back:
                        back_weight = back[node.name]
                        if back_weight is not None and weight is not None and back_weight == weight:
                            reciprocal_ok = True
                        break
                if not reciprocal_ok:
                    continue
                # Edge válida
                u, v = sorted((node.name, neighbor_name))
                valid_edges.add((u, v, float(weight)))

        # Crear aristas válidas; esto añade los nodos de forma implícita
        for u, v, w in valid_edges:
            self.graph.add_edge(u, v, weight=w)

        # No añadimos nodos aislados: sólo quedan los que participan en aristas
    
    async def get_shortest_path(self, source: str, target: str) -> Optional[GraphPath]:
        """Calcula el camino más corto entre dos nodos."""
        try:
            path = nx.shortest_path(self.graph, source=source, target=target, weight='weight')
            total_weight = nx.shortest_path_length(self.graph, source=source, target=target, weight='weight')
            return GraphPath(nodes=path, total_weight=total_weight)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None
    
    async def get_all_nodes(self) -> List[GraphNode]:
        """Obtiene todos los nodos del grafo."""
        nodes = []
        for node_name in self.graph.nodes():
            adjacent_nodes = await self.get_adjacent_nodes(node_name)  # Añadimos await aquí
            nodes.append(GraphNode(
                name=node_name,
                adjacent_nodes=adjacent_nodes  # Ahora sí es un dict, no una corrutina
            ))
        return nodes
    
    async def get_adjacent_nodes(self, node_name: str) -> Dict[str, float]:
        """Obtiene los nodos adyacentes a un nodo específico."""
        if node_name not in self.graph:
            return {}
        return {n: self.graph.edges[node_name, n]['weight'] for n in self.graph.neighbors(node_name)}