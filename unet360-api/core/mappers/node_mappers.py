from adapter.database.tag_repository import TagRepository

from core.dtos.node_dto import NodeOutDTO
from core.entities.node_model import Node

tag_repository = TagRepository()

async def transform_node_to_node_out_dto(node_db_obj: Node) -> NodeOutDTO:
    location_name = None

    if node_db_obj.location:
        try:
            resolved_location = await node_db_obj.location.fetch() 
            if resolved_location:
                location_name = resolved_location.name
        except Exception:
            location_name = None

    tags_names = []
    
    if node_db_obj.tags and len(node_db_obj.tags) > 0:
        resolved_tags = [await tag_repository.get_by_link(tag_link) for tag_link in node_db_obj.tags] 
        for tag_obj in resolved_tags:
            if tag_obj:
                tags_names.append(tag_obj.name)

    adyacent_names = []

    if node_db_obj.adyacent_nodes and not all(adyacent is None for adyacent in node_db_obj.adyacent_nodes):
        resolved_adyacents = [await adyacent_node.fetch() for adyacent_node in node_db_obj.adyacent_nodes]
        for adyacent_obj in resolved_adyacents:
            if adyacent_obj:
                adyacent_names.append(adyacent_obj.name)
            else:
                adyacent_names.append(None)
    
    if len(adyacent_names) < 4:
        adyacent_names.extend([None] * (4 - len(adyacent_names)))

    return NodeOutDTO(
        name=node_db_obj.name,
        location=location_name,
        url_image=node_db_obj.url_image,
        adyacent_nodes=adyacent_names,
        tags=tags_names
    )