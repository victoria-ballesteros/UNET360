from fastapi import APIRouter
from core.services.tenant_service import TenantService
from adapter.database.tenant_repository import TenantRepository
from core.dtos.tenant_dto import TenantCreateDTO, TenantOutDTO, TenantUpdateDTO
from typing import List

router = APIRouter(prefix="/tenants", tags=["Tenants"])
service = TenantService(TenantRepository())

# Crear un nuevo tenant
@router.post("/", response_model=TenantOutDTO)
async def create_tenant(dto: TenantCreateDTO):
    return await service.create_tenant(dto)

# Obtener tenant por supabase_user_id
@router.get("/{supabase_user_id}", response_model=TenantOutDTO)
async def get_tenant(supabase_user_id: str):
    return await service.get_tenant_by_supabase_user_id(supabase_user_id)

# Listar todos los tenants
@router.get("/", response_model=List[TenantOutDTO])
async def get_all_tenants():
    return await service.get_all_tenants()

# Actualizar tenant
@router.patch("/{supabase_user_id}", response_model=TenantOutDTO)
async def update_tenant(supabase_user_id: str, dto: TenantUpdateDTO):
    return await service.update_tenant(supabase_user_id, dto)

# Eliminar tenant
@router.delete("/{supabase_user_id}")
async def delete_tenant(supabase_user_id: str):
    return await service.delete_tenant(supabase_user_id)