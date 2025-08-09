from typing import Dict, Optional
from fastapi import HTTPException
from bson import ObjectId

from adapter.database.node_repository import NodeRepository
from adapter.database.tag_repository import TagRepository
from adapter.database.location_repository import LocationRepository

from core.dtos.node_dto import NodeCreateDTO, NodeUpdateDTO, NodeOutDTO, NodeStatusDTO
from core.entities.node_model import Node

from core.mappers.node_mappers import (transform_node_to_node_out_dto, update_db_obj)

from core.messages.error_messages import CREATE_ERROR_MESSAGE, OBJECT_NOT_FOUND_ERROR_MESSAGE

class NodeService:
    _instance: Optional["NodeService"] = None
    _repository_instance: Optional[NodeRepository] = None
    _location_repo_instance: Optional[LocationRepository] = None
    _tag_repo_instance: Optional[TagRepository] = None

    def __init__(self, repository: NodeRepository,
                 location_repo: LocationRepository,
                 tag_repo: TagRepository):
        self.repository = repository
        self.location_repo = location_repo
        self.tag_repo = tag_repo

    @property
    def node_repo(self):
        return self.repository


    async def create_node(self, new_node: NodeCreateDTO) -> NodeCreateDTO:
        location = None

        if new_node.location:
            location = await self.location_repo.get_by_name(new_node.location)
            if not location:
                raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)
            
        tags_dict = {}
        if new_node.tags:
            for tag_name, tag_values in new_node.tags.items():
                tag = await self.tag_repo.get_by_name(tag_name)
                if not tag:
                    raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)
                # tag_values expected as Dict[valueName, headingFloat]
                tags_dict[tag.name] = tag_values

        adjacent_nodes = []
        if new_node.adjacent_nodes:
            for adjacent in new_node.adjacent_nodes:
                adjacent_nodes.append(adjacent)
        else:
            adjacent_nodes = [None, None, None, None]

        node_db_obj = Node(
            name=new_node.name,
            location=location,
            url_image=new_node.url_image,
            adjacent_nodes=adjacent_nodes,
            arrow_angles=new_node.arrow_angles,
            forward_heading=new_node.forward_heading,
            tags=tags_dict,
            minimap=new_node.minimap if new_node.minimap is not None else {"image": "missing.png", "x": 0, "y": 0}
        )

        new_node_db_obj = await self.repository.create(new_node=node_db_obj)

        if not new_node_db_obj.id:
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE)
        
        return NodeCreateDTO(
            name=new_node_db_obj.name,
            location=new_node_db_obj.location.name if new_node_db_obj.location else None,
            url_image=new_node_db_obj.url_image,
            adjacent_nodes=new_node_db_obj.adjacent_nodes,
            arrow_angles=new_node_db_obj.arrow_angles,
            forward_heading=new_node_db_obj.forward_heading,
            tags=new_node_db_obj.tags,
            minimap=getattr(new_node_db_obj, "minimap", None)
        )


    async def get_node_by_name(self, name: str) -> NodeOutDTO | None:
        node_db_obj = await self.repository.get_by_name(name=name)

        if not node_db_obj:
            raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)
        
        return await transform_node_to_node_out_dto(node_db_obj)
    

    async def get_all_nodes(self) -> list[NodeOutDTO]:
        nodes = await self.repository.get_all()
        return [await transform_node_to_node_out_dto(node) for node in nodes]
    

    async def update_node(self, name: str, dto: NodeUpdateDTO) -> NodeOutDTO:
        node = await self.repository.get_by_name(name)
        if not node:
            raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)
        
        update_data = dto.dict(exclude_unset=True)

        if 'tags' in update_data:
            tags_dict = {}
            for tag_name, tag_values in update_data['tags'].items():
                tag = await self.tag_repo.get_by_name(tag_name)
                if not tag:
                    raise HTTPException(status_code=404, detail=f"Tag '{tag_name}' no encontrado")
                tags_dict[tag_name] = tag_values
            update_data['tags'] = tags_dict

        if 'adjacent_nodes' in update_data:
            adjacent_nodes = []
            for adjacent in update_data['adjacent_nodes']:
                adjacent_nodes.append(adjacent)
            update_data['adjacent_nodes'] = adjacent_nodes

        node = await update_db_obj(node_db_obj=node, new_data=update_data)
        updated = await self.repository.update(node)

        return await transform_node_to_node_out_dto(updated) if updated else None
    

    async def delete_node(self, name: str):
        node = await self.repository.get_by_name(name)
        if not node:
            raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)
        await self.repository.delete(node)
        return {"message": "Node deleted"}

    async def get_nodes_statuses(self) -> list[NodeStatusDTO]:
        nodes = await self.repository.get_all()
        name_to_node = {n.name: n for n in nodes}

        def compute_status(n: Node) -> NodeStatusDTO:
            reasons: list[str] = []

            # ERROR checks: missing strictly required
            if not n.url_image:
                reasons.append("Falta la imagen (url_image).")
            # adjacent_nodes: require at least 1 non-null and proper structure
            non_null_adj = [a for a in (n.adjacent_nodes or []) if a]
            if len(non_null_adj) == 0:
                reasons.append("Debe haber al menos un nodo adyacente.")

            error = len(reasons) > 0

            # WARNING checks
            if not n.location:
                reasons.append("Falta la ubicación (location).")

            # arrow_angles parallelism with adjacent_nodes
            angles = getattr(n, 'arrow_angles', None)
            if angles is None or len(angles) < 4:
                reasons.append("La lista de ángulos (arrow_angles) está incompleta.")
            else:
                # verify angle present where adjacent exists
                for idx, adj in enumerate(n.adjacent_nodes or []):
                    if adj is not None and (idx >= len(angles) or angles[idx] is None):
                        reasons.append(f"Falta un ángulo en arrow_angles para la posición {idx + 1}.")
            
            # minimap default check
            mm = getattr(n, 'minimap', None) or {}
            if mm.get('image') == 'missing.png' and mm.get('x') in (0, None) and mm.get('y') in (0, None):
                reasons.append("Minimapa sin configurar (valores por defecto).")

            # Cross-check adjacent nodes existence and reciprocity
            for adj in (n.adjacent_nodes or []):
                if isinstance(adj, dict):
                    for adj_name in adj.keys():
                        adj_node = name_to_node.get(adj_name)
                        if not adj_node:
                            reasons.append(f"El nodo adyacente '{adj_name}' no existe.")
                        else:
                            # reciprocity: adj_node should reference back to n.name somewhere
                            has_back = False
                            for back in (adj_node.adjacent_nodes or []):
                                if isinstance(back, dict) and n.name in back:
                                    has_back = True
                                    break
                            if not has_back:
                                reasons.append(f"La adyacencia con '{adj_name}' no es recíproca.")

            status = "OK"
            if any(r for r in reasons if r in ("Falta la imagen (url_image).", "Debe haber al menos un nodo adyacente.")):
                status = "ERROR"
            elif reasons:
                status = "WARNING"

            return NodeStatusDTO(name=n.name, status=status, reasons=reasons if reasons else None)

        return [compute_status(n) for n in nodes]
