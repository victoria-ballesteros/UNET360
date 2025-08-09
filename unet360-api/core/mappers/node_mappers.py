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
    
    tags_dict = {}
    if node_db_obj.tags:
        for tag_name, values in node_db_obj.tags.items():
            if isinstance(values, dict):
                tags_dict[tag_name] = values
            elif isinstance(values, list):
                tags_dict[tag_name] = {v: 0.0 for v in values}
            else:
                tags_dict[tag_name] = {}

    # Process adjacent nodes (sin verificación, solo copia el valor)
    adjacent_nodes_with_weights = []
    if node_db_obj.adjacent_nodes:
        for adjacent in node_db_obj.adjacent_nodes:
            adjacent_nodes_with_weights.append(adjacent)
    if len(adjacent_nodes_with_weights) < 4:
        adjacent_nodes_with_weights.extend([None] * (4 - len(adjacent_nodes_with_weights)))

    return NodeOutDTO(
        name=node_db_obj.name,
        location=location_name,
        url_image=node_db_obj.url_image,
        adjacent_nodes=adjacent_nodes_with_weights,
        arrow_angles=getattr(node_db_obj, "arrow_angles", [0, 1.5707963267948966, 3.141592653589793, -1.5707963267948966]),
        forward_heading=getattr(node_db_obj, "forward_heading", 0.0),
        tags=tags_dict,
        minimap=getattr(node_db_obj, "minimap", None)
    )

async def update_db_obj(node_db_obj: Node, new_data: dict) -> None:
    if 'name' in new_data and node_db_obj.name != new_data['name']:
        node_db_obj.name = new_data['name']

    if 'location' in new_data and new_data['location'] is not None:
        # new_data['location'] is expected to be a string name; resolve to link
        loc = await location_repository.get_by_name(new_data['location'])
        if not loc:
            raise HTTPException(status_code=404, detail="LOCATION_NOT_FOUND")
        node_db_obj.location = loc

    if 'url_image' in new_data and node_db_obj.url_image != new_data['url_image']:
        node_db_obj.url_image = new_data['url_image']

    if 'adjacent_nodes' in new_data:
        node_db_obj.adjacent_nodes = list(new_data['adjacent_nodes'])

    if 'arrow_angles' in new_data:
        node_db_obj.arrow_angles = list(new_data['arrow_angles'])

    if 'forward_heading' in new_data:
        node_db_obj.forward_heading = float(new_data['forward_heading'])

    if 'tags' in new_data:
        # Validate tag names exist; values are dict[valueName -> headingFloat]
        tags_dict = {}
        for tag_name, tag_values in new_data['tags'].items():
            tag = await tag_repository.get_by_name(tag_name)
            if not tag:
                raise HTTPException(status_code=404, detail=f"TAG_NOT_FOUND: {tag_name}")
            tags_dict[tag_name] = tag_values
        node_db_obj.tags = tags_dict

    if 'minimap' in new_data:
        node_db_obj.minimap = new_data['minimap']

    return node_db_obj
