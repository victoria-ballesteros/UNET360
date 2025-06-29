from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Any

from core.dtos.responses_dto import GeneralResponse 

from core.services.tag_service import TagService
from adapter.database.tag_repository import TagRepository
from core.dtos.tag_dto import TagCreateDTO, TagOutDTO, TagUpdateDTO


router = APIRouter(prefix="/tags", tags=["Tags"])

service = TagService(TagRepository()) 

@router.post("/", response_model=GeneralResponse)
async def create_tags(dto: TagCreateDTO):
    try:
        created_tag_dto = await service.create_tag(dto) 
        
        return GeneralResponse(
            http_code=status.HTTP_201_CREATED,
            status=True,
            response_obj=created_tag_dto.model_dump()
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
async def get_tag(name: str):
    try:
        tag_out_dto = await service.get_tag_by_name(name)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=tag_out_dto.model_dump() if tag_out_dto else None
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
async def get_all_tags():
    try:
        tags_out_dtos = await service.get_all_tags()
        
        tags_data_list = [tag_dto.model_dump() for tag_dto in tags_out_dtos]
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=tags_data_list
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
async def update_tag(name: str, dto: TagUpdateDTO):
    try:
        updated_tag_dto = await service.update_tag(name, dto)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=updated_tag_dto.model_dump()
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
async def delete_tag(name: str):
    try:
        delete_result = await service.delete_tag(name)
        
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