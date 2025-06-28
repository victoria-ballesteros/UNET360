from typing import Optional
from fastapi import HTTPException

from adapter.database.node_repository import NodeRepository
from adapter.database.tag_repository import TagRepository
from adapter.database.location_repository import LocationRepository
from core.dtos.node_dto import NodeCreateDTO, NodeUpdateDTO, NodeOutDTO
from core.entities.node_model import Node
from core.messages.error_messages import CREATE_ERROR_MESSAGE
from core.mappers.node_mappers import transform_node_to_node_out_dto

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
                raise HTTPException(status_code=404, detail=f"Location '{new_node.location}' not found")
            
        tags = []
        if new_node.tags:
            for tag_name in new_node.tags:
                tag = await self.tag_repo.get_by_name(tag_name)
                if not tag:
                    raise HTTPException(status_code=404, detail=f"Tag '{tag_name}' not found")
                tags.append(tag)

        adyacents = []
        if new_node.adyacent_nodes:
            for name in new_node.adyacent_nodes:
                if name:
                    node = await self.node_repo.get_by_name(name)
                    if not node:
                        raise HTTPException(status_code=404, detail=f"Adyacent node '{name}' not found")
                    adyacents.append(node)
                else:
                    adyacents.append(None)
        else:
            adyacents = [None, None, None, None]

        node_db_obj = Node(name=new_node.name,
                           location=location,
                           url_image=new_node.url_image,
                           adyacent_nodes=adyacents,
                           tags=tags)
        new_node_db_obj = await self.repository.create(new_node=node_db_obj)

        if not new_node_db_obj.id:
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE)
        
        location_name = new_node_db_obj.location.name if new_node_db_obj.location else None
        tags_names = [tag.name for tag in new_node_db_obj.tags] if new_node_db_obj.tags else []
        adyacent_names = [
            adj.name if adj is not None else None
            for adj in (new_node_db_obj.adyacent_nodes or [None, None, None, None])
        ]


        return NodeCreateDTO(
        name=new_node_db_obj.name,
        location=location_name,
        url_image=new_node_db_obj.url_image,
        adyacent_nodes=adyacent_names,
        tags=tags_names,
        )


    async def get_node_by_name(self, name: str) -> NodeOutDTO | None:
        node_db_obj = await self.repository.get_by_name(name=name)

        if not node_db_obj:
            raise HTTPException(status_code=404, detail="node not found")
        
        return await transform_node_to_node_out_dto(node_db_obj)
    

    async def get_all_nodes(self) -> list[NodeOutDTO]:
        nodes = await self.repository.get_all()
        return [await transform_node_to_node_out_dto(node) for node in nodes]
    

    async def update_node(self, name: str, dto: NodeUpdateDTO) -> NodeOutDTO:
        node = await self.repository.get_by_name(name)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found")
     
        update_data = dto.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(node, key, value)
        print(node)
        updated = await self.repository.update(node)
        
        return [await transform_node_to_node_out_dto(updated)] if updated else None
    

    async def delete_node(self, name: str):
        node = await self.repository.get_by_name(name)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found")
        await self.repository.delete(node)
        return {"message": "Node deleted"}