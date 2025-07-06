from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from core.exceptions.graph_exceptions import NodeNotFoundError, NoPathFoundError

class GraphServicePort(ABC):
    """Interfaz que define las operaciones del servicio de grafos."""

    @abstractmethod
    def shortest_path(self, start: str, end: str) -> List[str]:
        """Devuelve el camino más corto entre dos nodos.
        
        Args:
            start (str): ID del nodo inicial.
            end (str): ID del nodo destino.
        
        Returns:
            List[str]: Secuencia de nodos desde 'start' hasta 'end'.
        
        Raises:
            NodeNotFoundError: Si algún nodo no existe.
            NoPathFoundError: Si no hay ruta posible.
        """
        pass  # ¡Sí, aquí va pass! (solo es una definición)

    @abstractmethod
    def sequential_path(self, nodes: List[str]) -> List[str]:
        """Calcula una ruta secuencial a través de múltiples nodos.
        
        Args:
            nodes (List[str]): Lista de nodos a recorrer en orden.
        
        Returns:
            List[str]: Ruta completa que pasa por todos los nodos.
        """
        pass

    @abstractmethod
    def update_graph(self, updates: Dict[str, Any]) -> None:
        """Actualiza el grafo añadiendo/eliminando nodos o conexiones.
        
        Args:
            updates (Dict[str, Any]): Datos para actualizar el grafo.
        """
        pass