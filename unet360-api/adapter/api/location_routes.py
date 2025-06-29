from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Any

from core.dtos.responses_dto import GeneralResponse 

from core.services.location_service import LocationService
from adapter.database.location_repository import LocationRepository
from core.dtos.location_dto import LocationCreateDTO, LocationOutDTO, LocationUpdateDTO


router = APIRouter(prefix="/locations", tags=["Locations"])

service = LocationService(LocationRepository()) 

@router.post("/", response_model=GeneralResponse)
async def create_locations(dto: LocationCreateDTO):
    try:
        created_location_dto = await service.create_location(dto) 
        
        return GeneralResponse(
            http_code=status.HTTP_201_CREATED,
            status=True,
            response_obj=created_location_dto.model_dump()
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.get("/{name}", response_model=GeneralResponse)
async def get_location(name: str):
    try:
        location_out_dto = await service.get_location_by_name(name)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=location_out_dto.model_dump() if location_out_dto else None
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.get("/", response_model=GeneralResponse)
async def get_all_locations():
    try:
        locations_out_dtos = await service.get_all_locations()
        
        locations_data_list = [loc_dto.model_dump() for loc_dto in locations_out_dtos]
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=locations_data_list
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.patch("/{name}", response_model=GeneralResponse)
async def update_location(name: str, dto: LocationUpdateDTO):
    try:
        updated_location_dto = await service.update_location(name, dto)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=updated_location_dto.model_dump()
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.delete("/{name}", response_model=GeneralResponse)
async def delete_location(name: str):
    try:
        delete_result = await service.delete_location(name)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK, 
            status=True,
            response_obj=delete_result
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )