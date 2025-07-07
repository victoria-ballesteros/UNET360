from fastapi import HTTPException
from bson import ObjectId
from beanie.odm.fields import Link

from adapter.database.tag_repository import TagRepository
from adapter.database.location_repository import LocationRepository
from adapter.database.node_repository import NodeRepository

from core.dtos.node_dto import NodeOutDTO
from core.entities.node_model import Node
from core.entities.location_model import Location
from core.entities.tag_model import Tag

tag_repository = TagRepository()
location_repository = LocationRepository()
node_repository = NodeRepository()

async def force_to_link(obj, repository, model_class):
    if obj is None:
        return None
    if isinstance(obj, Link):
        return obj
    if isinstance(obj, ObjectId):
        document = await repository.get_by_id(obj)
        if document:
            return document.to_ref()
        else:
            raise HTTPException(status_code=404, detail=f"DOCUMENT_NOT_FOUND: {obj}")
    if isinstance(obj, model_class):
        return obj
    
    raise HTTPException(status_code=404, detail=f"UNRECOGNIZABLE_OBJECT_TYPE: {obj}")


async def transform_node_to_node_out_dto(node_db_obj: Node) -> NodeOutDTO:
    location_name = None

    if node_db_obj.location:
        try:
            if not hasattr(node_db_obj.location, "id"):
                resolved_location = await location_repository.get_by_link(await force_to_link(node_db_obj.location, location_repository, Location))        
            else:
                resolved_location = node_db_obj.location
        
            if resolved_location:
                location_name = resolved_location.name
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"FAILED_TO_FETCH_LOCATION: {e!s}")
    
    #Process tags
    tags_dict = {}
    if node_db_obj.tags:
        tags_dict = node_db_obj.tags

    # Process adyacent nodes
    adjacent_nodes_with_weights = []
    if node_db_obj.adjacent_nodes:
        for adjacent in node_db_obj.adjacent_nodes:
            if adjacent is None:
                adjacent_nodes_with_weights.append(None)
                continue
            
            try:
                # Cada adjacent es un dict {node_id: weight}
                node_name = next(iter(adjacent.keys())) if adjacent else None
                weight = adjacent[node_name] if node_name else None
                
                if node_name:
                    node_obj = await node_repository.get_by_name(node_name)
                    if node_obj:
                        adjacent_nodes_with_weights.append({node_obj.name: weight})
                    else:
                        adjacent_nodes_with_weights.append(None)
                else:
                    adjacent_nodes_with_weights.append(None)
            except Exception as e:
                raise HTTPException(
                    status_code=404, 
                    detail=f"FAILED_TO_FETCH_ADJACENT_NODES: {e!s}"
                )

    
    if len(adjacent_nodes_with_weights) < 4:
        adjacent_nodes_with_weights.extend([None] * (4 - len(adjacent_nodes_with_weights)))

    return NodeOutDTO(
        name=node_db_obj.name,
        location=location_name,
        url_image=node_db_obj.url_image,
        adjacent_nodes=adjacent_nodes_with_weights,
        tags=tags_dict
    )
async def update_db_obj(node_db_obj: Node, new_data: dict) -> Node:
    if 'name' in new_data and node_db_obj.name != new_data['name']:
        node_db_obj.name = new_data['name']


    if 'location' in new_data:
        if new_data['location'] is None:
            node_db_obj.location = None
        else:
            if node_db_obj.location:
                current_location = await location_repository.get_by_link(node_db_obj.location)
                if not current_location or current_location.name != new_data['location']:
                    new_location = await location_repository.get_by_name(new_data['location'])
                    if not new_location:
                        raise HTTPException(status_code=404, detail="LOCATION_NOT_FOUND")
                    node_db_obj.location = new_location
            else:
                new_location = await location_repository.get_by_name(new_data['location'])
                if not new_location:
                    raise HTTPException(status_code=404, detail="LOCATION_NOT_FOUND")
                node_db_obj.location = new_location

    if 'url_image' in new_data and node_db_obj.url_image != new_data['url_image']:
        node_db_obj.url_image = new_data['url_image']

    if 'adjacent_nodes' in new_data:
        adjacent_nodes = []
        for adjacent in new_data['adjacent_nodes']:
            if adjacent is not None:
                node_name = next(iter(adjacent.keys())) if adjacent else None
                weight = adjacent[node_name] if node_name else None
                
                if node_name:
                    adj_node = await node_repository.get_by_name(node_name)
                    if not adj_node:
                        raise HTTPException(
                            status_code=404, 
                            detail=f"NODE_NOT_FOUND: {node_name}"
                        )
                    adjacent_nodes.append({node_name: weight})
                else:
                    adjacent_nodes.append(None)
            else:
                adjacent_nodes.append(None)
        node_db_obj.adjacent_nodes = adjacent_nodes

    if 'tags' in new_data:
        tags_dict = {}
        for tag_name, tag_values in new_data['tags'].items():
            tag = await tag_repository.get_by_name(tag_name)
            if not tag:
                raise HTTPException(
                    status_code=404, 
                    detail=f"TAG_NOT_FOUND: {tag_name}"
                )
            tags_dict[tag_name] = tag_values
        node_db_obj.tags = tags_dict

    return node_db_obj