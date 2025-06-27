from fastapi import APIRouter
from core.services.node_service import NodeService
from adapter.database.node_repository import NodeRepository
from adapter.database.location_repository import LocationRepository
from adapter.database.tag_repository import TagRepository
from core.dtos.node_dto import NodeCreateDTO, NodeOutDTO, NodeUpdateDTO
from typing import List

router = APIRouter(prefix="/nodes", tags=["Nodes"])
service = NodeService(NodeRepository(), LocationRepository(), TagRepository())

# Crear un nuevo nodo
@router.post("/", response_model=NodeOutDTO)
async def create_node(dto: NodeCreateDTO):
    return await service.create_node(dto)

# Obtener nodo por nombre
@router.get("/{name}", response_model=NodeOutDTO)
async def get_node(name: str):
    return await service.get_node_by_name(name)

# Listar todos los nodos
@router.get("/", response_model=List[NodeOutDTO])
async def get_all_nodes():
    return await service.get_all_nodes()

# Actualizar nodo
@router.patch("/{name}", response_model=NodeOutDTO)
async def update_node(name: str, dto: NodeUpdateDTO):
    return await service.update_node(name, dto)

# Eliminar nodo
@router.delete("/{name}")
async def delete_node(name: str):
    return await service.delete_node(name)