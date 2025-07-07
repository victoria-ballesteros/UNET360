from fastapi import APIRouter, Depends, HTTPException
from core.services.graph_service import GraphService
from core.ports.graph_service_port import GraphServicePort
from adapter.external.graph_adapter import NetworkXGraphService
from adapter.database.node_repository import NodeRepository
from core.dtos.responses_dto import GeneralResponse
from core.exceptions.graph_exceptions import NodeNotFoundError, NoPathError  # Adjust the import path as needed

router = APIRouter(prefix="/graph", tags=["Graph"])

def get_node_repository() -> NodeRepository:
    return NodeRepository()

def get_graph_adapter(node_repo: NodeRepository = Depends(get_node_repository)) -> GraphServicePort:
    """Devuelve el adaptador concreto"""
    return NetworkXGraphService(node_repo)

def get_graph_service(adapter: GraphServicePort = Depends(get_graph_adapter)) -> GraphService:
    """Envuelve el adaptador en el servicio de negocio"""
    return GraphService(adapter)

@router.on_event("startup")
async def startup_event():
    node_repo = NodeRepository()
    graph_service = NetworkXGraphService(node_repo)
    await graph_service.refresh_graph()

@router.get("/shortest-path/{source}/{target}", response_model=GeneralResponse)
async def get_shortest_path(source: str, target: str, graph_service: GraphService = Depends(get_graph_service)):
    try:
        path = await graph_service.calculate_shortest_path(source, target)
        return GeneralResponse(
            http_code=200,
            status=True,
            response_obj={
                "path": path.nodes,
                "total_weight": path.total_weight
            }
        )
    except NodeNotFoundError as e:
        return GeneralResponse(
            http_code=404,
            status=False,
            response_obj={"message": str(e)}
        )
    except NoPathError as e:
        return GeneralResponse(
            http_code=404,
            status=False,
            response_obj={"message": str(e)}
        )

@router.post("/refresh", response_model=GeneralResponse)
async def refresh_graph(graph_service: GraphService = Depends(get_graph_service)):
    await graph_service.refresh_graph()
    return GeneralResponse(
        http_code=200,
        status=True,
        response_obj={"message": "Graph refreshed successfully"}
    )

@router.get("/nodes", response_model=GeneralResponse)
async def get_all_nodes(graph_service: GraphService = Depends(get_graph_service)):
    nodes = await graph_service.get_all_nodes()
    return GeneralResponse(
        http_code=200,
        status=True,
        response_obj=[node.dict() for node in nodes]
    )

@router.get("/nodes/{node_name}/adjacent", response_model=GeneralResponse)
async def get_adjacent_nodes(node_name: str, graph_service: GraphService = Depends(get_graph_service)):
    try:
        adjacent = await graph_service.get_adjacent_nodes(node_name)
        return GeneralResponse(
            http_code=200,
            status=True,
            response_obj=adjacent
        )
    except NodeNotFoundError as e:
        return GeneralResponse(
            http_code=404,
            status=False,
            response_obj={"message": str(e)}
        )