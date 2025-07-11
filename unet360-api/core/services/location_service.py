from typing import Optional
from fastapi import HTTPException

from adapter.database.location_repository import LocationRepository
from core.dtos.location_dto import LocationCreateDTO, LocationUpdateDTO, LocationOutDTO
from core.entities.location_model import Location
from core.messages.error_messages import CREATE_ERROR_MESSAGE, OBJECT_NOT_FOUND_ERROR_MESSAGE


class LocationService:
    _instance: Optional["LocationService"] = None
    _repository_instance: Optional[LocationRepository] = None

    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def create_location(
        self, new_location: LocationCreateDTO
    ) -> LocationOutDTO:
        location_db_obj = Location(**new_location.model_dump())
        new_location_db_obj = await self.repository.create(new_location=location_db_obj)

        if not new_location_db_obj.id:
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE)

        return LocationOutDTO(**new_location_db_obj.model_dump())

    async def get_location_by_name(self, name: str) -> LocationOutDTO | None:
        location_db_obj = await self.repository.get_by_name(name=name)

        if not location_db_obj:
            raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)

        return LocationOutDTO(**location_db_obj.model_dump())

    async def get_all_locations(self) -> list[LocationOutDTO]:
        locations = await self.repository.get_all()
        return [LocationOutDTO(**loc.model_dump()) for loc in locations]

    async def update_location(self, name: str, dto: LocationUpdateDTO) -> LocationOutDTO:
        location = await self.repository.get_by_name(name)
        if not location:
            raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)

        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(location, key, value)

        updated = await self.repository.update(location)
        return LocationOutDTO(**updated.model_dump())

    async def delete_location(self, name: str):
        location = await self.repository.get_by_name(name)
        if not location:
            raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)
        await self.repository.delete(location)
        return {"message": "Location deleted"}