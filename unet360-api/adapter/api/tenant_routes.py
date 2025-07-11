from fastapi import APIRouter, HTTPException, status
from typing import List, Optional, Any

from core.dtos.responses_dto import GeneralResponse 

from core.services.tenant_service import TenantService
from adapter.database.tenant_repository import TenantRepository
from core.dtos.tenant_dto import TenantCreateDTO, TenantOutDTO, TenantUpdateDTO


router = APIRouter(prefix="/tenants", tags=["Tenants"])

service = TenantService(TenantRepository()) 

@router.post("/", response_model=GeneralResponse)
async def create_tenant(dto: TenantCreateDTO):
    try:
        created_tenant_dto = await service.create_tenant(dto) 
        
        return GeneralResponse(
            http_code=status.HTTP_201_CREATED,
            status=True,
            response_obj=created_tenant_dto.model_dump()
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

@router.get("/{supabase_user_id}", response_model=GeneralResponse)
async def get_tenant(supabase_user_id: str):
    try:
        tenant_out_dto = await service.get_tenant_by_supabase_user_id(supabase_user_id)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=tenant_out_dto.model_dump() if tenant_out_dto else None
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
async def get_all_tenants():
    try:
        tenants_out_dtos = await service.get_all_tenants()
        
        tenants_data_list = [tenant_dto.model_dump() for tenant_dto in tenants_out_dtos]
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=tenants_data_list
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

@router.patch("/{supabase_user_id}", response_model=GeneralResponse)
async def update_tenant(supabase_user_id: str, dto: TenantUpdateDTO):
    try:
        updated_tenant_dto = await service.update_tenant(supabase_user_id, dto)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=updated_tenant_dto.model_dump()
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

@router.delete("/{supabase_user_id}", response_model=GeneralResponse)
async def delete_tenant(supabase_user_id: str):
    try:
        delete_result = await service.delete_tenant(supabase_user_id)
        
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