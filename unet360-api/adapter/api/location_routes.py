from fastapi import APIRouter
from core.services.location_service import LocationService
from adapter.database.location_repository import LocationRepository
from core.dtos.location_dto import LocationCreateDTO, LocationOutDTO, LocationUpdateDTO
from pymongo.errors import DuplicateKeyError
from typing import List

router = APIRouter(prefix="/locations", tags=["Locations"])
service = LocationService(LocationRepository())

# Crear una nueva ubicación
@router.post("/", response_model=LocationOutDTO)
async def create_locations(dto: LocationCreateDTO):
    return await service.create_location(dto)

# Obtener ubicación por nombre
@router.get("/{name}", response_model=LocationOutDTO)
async def get_location(name: str):
    return await service.get_location_by_name(name)

# Listar todas las ubicaciones
@router.get("/", response_model=List[LocationOutDTO])
async def get_all_locations():
    return await service.get_all_locations()

# Actualizar ubicación
@router.patch("/{name}", response_model=LocationOutDTO)
async def update_location(name: str, dto: LocationUpdateDTO):
    return await service.update_location(name, dto)

# Eliminar ubicación
@router.delete("/{name}")
async def delete_location(name: str):
    return await service.delete_location(name)