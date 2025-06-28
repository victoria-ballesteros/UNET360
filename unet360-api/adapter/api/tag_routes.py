from fastapi import APIRouter
from core.services.tag_service import TagService
from adapter.database.tag_repository import TagRepository
from core.dtos.tag_dto import TagCreateDTO, TagOutDTO, TagUpdateDTO
from typing import List

router = APIRouter(prefix="/tags", tags=["Tags"])
service = TagService(TagRepository())

# Crear un nuevo tag
@router.post("/", response_model=TagOutDTO)
async def create_tags(dto: TagCreateDTO):
    return await service.create_tag(dto)

# Obtener tag por nombre
@router.get("/{name}", response_model=TagOutDTO)
async def get_tag(name: str):
    return await service.get_tag_by_name(name)

# Listar todos los tags
@router.get("/", response_model=List[TagOutDTO])
async def get_all_tags():
    return await service.get_all_tags()

# Actualizar tag
@router.patch("/{name}", response_model=TagOutDTO)
async def update_tag(name: str, dto: TagUpdateDTO):
    return await service.update_tag(name, dto)

# Eliminar tag
@router.delete("/{name}")
async def delete_tag(name: str):
    return await service.delete_tag(name)