from typing import Dict, Optional
from fastapi import HTTPException
from bson import ObjectId

from adapter.database.node_repository import NodeRepository
from adapter.database.tag_repository import TagRepository
from adapter.database.location_repository import LocationRepository

from core.dtos.node_dto import NodeCreateDTO, NodeUpdateDTO, NodeOutDTO
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
                tags_dict[tag.name] = tag_values

        adjacent_nodes = []
        if new_node.adjacent_nodes:
            for adjacent in new_node.adjacent_nodes:
                if adjacent is not None:
                    node_name = next(iter(adjacent.keys()))
                    weight = adjacent[node_name]

                    node = await self.node_repo.get_by_name(node_name)
                    
                    if not node:
                        raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)
                    
                    adjacent_nodes.append({node_name: weight})
                else:
                    adjacent_nodes.append(None)
        else:
            adjacent_nodes = [None, None, None, None]

        node_db_obj = Node(
            name=new_node.name,
            location=location,
            url_image=new_node.url_image,
            adjacent_nodes=adjacent_nodes,
            tags=tags_dict

        )

        new_node_db_obj = await self.repository.create(new_node=node_db_obj)

        if not new_node_db_obj.id:
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE)
        
        

        return NodeCreateDTO(
            name=new_node_db_obj.name,
            location=new_node_db_obj.location.name if new_node_db_obj.location else None,
            url_image=new_node_db_obj.url_image,
            adjacent_nodes=new_node_db_obj.adjacent_nodes,
            tags=new_node_db_obj.tags
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

        # Procesamiento especial para location si viene en el update
        if 'location' in update_data and update_data['location'] is not None:
            # Verificar que la ubicación exista en la base de datos
            location = await self.location_repo.get_by_name(update_data['location'])
            if not location:
                raise HTTPException(status_code=404, detail="Location not found")
            update_data['location'] = location
        elif 'location' in update_data:
            update_data['location'] = None
            
        # Procesamiento especial para tags si vienen en el update
        if 'tags' in update_data:
            tags_dict = {}
            for tag_name, tag_values in update_data['tags'].items():
                
                # Verificar que el tag exista en la base de datos
                tag = await self.tag_repo.get_by_name(tag_name)
                if not tag:
                    raise HTTPException(status_code=404, detail=f"Tag '{tag_name}' no encontrado")
                tags_dict[tag_name] = tag_values
            update_data['tags'] = tags_dict

        # Procesamiento especial para adjacent_nodes si vienen en el update
        if 'adjacent_nodes' in update_data:
            adjacent_nodes = []
            for adjacent in update_data['adjacent_nodes']:
                if adjacent is not None:
                    node_name = next(iter(adjacent.keys())) if adjacent else None
                    weight = adjacent[node_name] if node_name else None

                    # Verificar que el nodo adyacente exista en la base de datos
                    adj_node = await self.node_repo.get_by_name(node_name)
                    if not adj_node:
                        raise HTTPException(status_code=404, detail=f"Nodo adyacente '{node_name}' no encontrado")
                    
                    adjacent_nodes.append({node_name: weight})

                else:
                    adjacent_nodes.append(None)
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