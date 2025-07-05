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
    
    tags_names = []

    if node_db_obj.tags and len(node_db_obj.tags) > 0:
        resolved_tags = []
        for tag_link in node_db_obj.tags:
            try:
                if not hasattr(tag_link, "id"):
                    tag_obj = await tag_repository.get_by_link(await force_to_link(tag_link, tag_repository, Tag))
                else:
                    tag_obj = tag_link
        
                if tag_obj:
                    resolved_tags.append(tag_obj.name)
            except Exception as e:
                raise HTTPException(status_code=404, detail=f"FAILED_TO_FETCH_TAGS: {e!s}")
    
        tags_names = resolved_tags

    adyacent_names = []

    if node_db_obj.adyacent_nodes:
        for adyacent_obj in node_db_obj.adyacent_nodes:
            if adyacent_obj is None:
                adyacent_names.append(None)
                continue

            try:
                if not hasattr(adyacent_obj, "id"):
                    forced_link = await force_to_link(adyacent_obj, node_repository, Node)
                    resolved_node = await node_repository.get_by_link(forced_link)
                else:
                    resolved_node = adyacent_obj

                if resolved_node:
                    adyacent_names.append(resolved_node.name)
                else:
                    adyacent_names.append(None)
            except Exception:
                raise HTTPException(status_code=404, detail=f"FAILED_TO_FETCH_ADYACENT_NODES: {e!s}")
    
    if len(adyacent_names) < 4:
        adyacent_names.extend([None] * (4 - len(adyacent_names)))

    return NodeOutDTO(
        name=node_db_obj.name,
        location=location_name,
        url_image=node_db_obj.url_image,
        adyacent_nodes=adyacent_names,
        tags=tags_names
    )

async def update_db_obj(node_db_obj: Node, new_data: dict) -> None:
    if node_db_obj.name != new_data['name']:
        node_db_obj.name = new_data['name']

    new_location = await location_repository.get_by_link(node_db_obj.location)

    if not new_location:
        raise HTTPException(status_code=404, detail="LOCATION_NOT_FOUND")
        
    if node_db_obj.location != new_location.id:
        node_db_obj.location = new_location

    if node_db_obj.url_image != new_data['url_image']:
        node_db_obj.url_image = new_data['url_image']

    updated_adyacent_nodes = []

    for adyacent_node_name in new_data.get('adyacent_nodes', []):
        if adyacent_node_name is not None:
            new_adyacent_node = await node_repository.get_by_name(adyacent_node_name)
            if not new_adyacent_node:
                raise HTTPException(status_code=404, detail=f"NODE_NOT_FOUND: {adyacent_node_name}")
            updated_adyacent_nodes.append(new_adyacent_node)
        else:
            updated_adyacent_nodes.append(None)

    node_db_obj.adyacent_nodes = updated_adyacent_nodes

    updated_tags = []

    for tag_name in new_data.get('tags', []):
        new_tag = await tag_repository.get_by_name(tag_name)
        if not new_tag:
            raise HTTPException(status_code=404, detail=f"TAG_NOT_FOUND: {tag_name}")
        updated_tags.append(new_tag)

    node_db_obj.tags = updated_tags

    return node_db_obj
