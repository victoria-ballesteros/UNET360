from core.entities.location_model import Location

class LocationRepository:
    async def create(self, new_location: Location) -> Location | None:
        return await new_location.insert()
    
    async def get_by_name(self, name: str) -> Location | None:
        return await Location.find_one(Location.name == name)
    
    async def get_all(self) -> list[Location]:
        return await Location.find_all().to_list()
    
    async def update(self, location: Location) -> Location | None:
        return await location.save()
    
    async def delete(self, location: Location) -> None:
        await location.delete()
