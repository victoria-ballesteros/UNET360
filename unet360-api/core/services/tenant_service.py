from typing import Optional
from fastapi import HTTPException

from adapter.database.tenant_repository import TenantRepository
from core.dtos.tenant_dto import TenantCreateDTO, TenantUpdateDTO, TenantOutDTO
from core.entities.tenant_model import Tenant
from core.messages.error_messages import CREATE_ERROR_MESSAGE


class TenantService:
    _instance: Optional["TenantService"] = None
    _repository_instance: Optional[TenantRepository] = None

    def __init__(self, repository: TenantRepository):
        self.repository = repository

    async def create_tenant(self, new_tenant: TenantCreateDTO) -> TenantOutDTO:
        tenant_db_obj = Tenant(**{**new_tenant.dict(exclude_none=True)})
        new_tenant_db_obj = await self.repository.create(new_tenant=tenant_db_obj)

        if not new_tenant_db_obj.id:
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE)

        return TenantOutDTO(**new_tenant_db_obj.dict())

    async def get_tenant_by_supabase_user_id(self, supabase_user_id: str) -> TenantOutDTO | None:
        tenant_db_obj = await self.repository.get_by_supabase_user_id(supabase_user_id=supabase_user_id)

        if not tenant_db_obj:
            raise HTTPException(status_code=404, detail="tenant not found")

        return TenantOutDTO(**tenant_db_obj.dict())

    async def get_all_tenants(self) -> list[TenantOutDTO]:
        tenants = await self.repository.get_all()
        return [TenantOutDTO(**tenant.dict()) for tenant in tenants]

    async def update_tenant(self, supabase_user_id: str, dto: TenantUpdateDTO) -> TenantOutDTO:
        tenant = await self.repository.get_by_supabase_user_id(supabase_user_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        update_data = dto.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tenant, key, value)

        updated = await self.repository.update(tenant)
        return TenantOutDTO(**updated.dict())

    async def delete_tenant(self, supabase_user_id: str):
        tenant = await self.repository.get_by_supabase_user_id(supabase_user_id)
        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")
        await self.repository.delete(tenant)
        return {"message": "Tenant deleted"}