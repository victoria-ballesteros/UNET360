class GraphException(Exception):
    """Base exception para todos los errores de grafo"""

    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details if details is not None else {}
        super().__init__(message)

class NodeNotFoundError(GraphException):
    """Cuando un nodo no existe en el grafo"""
    def __init__(self, node_id: str, graph_id: str = "default"):
        super().__init__(
            message=f"Nodo '{node_id}' no encontrado en el grafo '{graph_id}'.",
            details={
                "node_id": node_id,
                "graph_id": graph_id,
                "error_code": "GRAPH_001"
            }
        )
    
class NoPathFoundError(GraphException):
    """Cuando no existe un camino entre dos nodos en el grafo"""
    def __init__(self, start: str, end: str, graph_id: str = "default"):
        super().__init__(
            message=f"No hay ruta valida entre '{start}' y '{end}' en el grafo '{graph_id}'.",
            details={
                "start_node_id": start,
                "end_node_id": end,
                "graph_id": graph_id,
                "error_code": "GRAPH_002"
            }
        )