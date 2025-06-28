# filename: core/dtos/node_mappers.py

from typing import List, Optional
from pydantic import BaseModel

from core.dtos.node_dto import NodeOutDTO
from core.entities.node_model import Node
from core.entities.location_model import Location # Necesario para el type hint y si fetchamos
from core.entities.tag_model import Tag         # Necesario para el type hint y si fetchamos

async def transform_node_to_node_out_dto(node_db_obj: Node) -> NodeOutDTO:
    location_name = None
    if node_db_obj.location:
        # Intenta cargar la ubicación si no está ya cargada
        # Si ya está cargada (es una instancia de Location), fetch() no hará nada
        # Si no existe, fetch() puede devolver None o lanzar una excepción,
        # dependiendo de la configuración de Beanie. Aquí asumimos que devuelve None si no encuentra.
        try:
            # Asegurarse de que el Link esté resuelto
            # Si node_db_obj.location es solo un DBRef, .fetch() lo resolverá.
            # Si ya es un objeto, .fetch() devolverá el mismo objeto.
            resolved_location = await node_db_obj.location.fetch() 
            if resolved_location:
                location_name = resolved_location.name
        except Exception: # Captura cualquier error si el Link es inválido o no se resuelve
            location_name = None # O loguear el error

    tags_names = []
    if node_db_obj.tags:
        # Fetch all tags if they are not loaded
        # .fetch_all() asegura que todos los links en la lista sean resueltos
        # Devuelve una lista de los objetos Tag resueltos
        resolved_tags = await node_db_obj.tags.fetch_all() 
        for tag_obj in resolved_tags:
            if tag_obj: # Asegurarse de que el objeto Tag realmente se haya resuelto
                tags_names.append(tag_obj.name)

    adyacent_names = []
    if node_db_obj.adyacent_nodes:
        # Fetch all adyacent nodes if they are not loaded
        resolved_adyacents = await node_db_obj.adyacent_nodes.fetch_all()
        for adyacent_obj in resolved_adyacents:
            if adyacent_obj:
                adyacent_names.append(adyacent_obj.name)
            else:
                adyacent_names.append(None) # Si el link es None, o si fetch_all devuelve None para un link nulo
    
    if len(adyacent_names) < 4:
        adyacent_names.extend([None] * (4 - len(adyacent_names)))

    return NodeOutDTO(
        name=node_db_obj.name,
        location=location_name,
        url_image=node_db_obj.url_image,
        adyacent_nodes=adyacent_names,
        tags=tags_names
    )