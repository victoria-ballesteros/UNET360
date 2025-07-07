class GraphException(Exception):
    """Base exception for graph-related errors"""
    pass

class NodeNotFoundError(GraphException):
    def __init__(self, node_name: str):
        self.node_name = node_name
        super().__init__(f"Node '{node_name}' not found in graph")

class NoPathError(GraphException):
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target
        super().__init__(f"No path exists between '{source}' and '{target}'")