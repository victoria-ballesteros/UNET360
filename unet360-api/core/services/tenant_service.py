# unet360-api/core/services/tenant_service.py

from typing import Optional, List
from fastapi import HTTPException, status
import logging
from supabase import Client as SupabaseClient
from gotrue.errors import AuthApiError
from datetime import datetime, timedelta, timezone

from adapter.database.tenant_repository import TenantRepository
from core.dtos.tenant_dto import TenantCreateDTO, TenantUpdateDTO, TenantOutDTO, TenantStatusDTO
from core.entities.tenant_model import Tenant
from core.messages.error_messages import CREATE_ERROR_MESSAGE, OBJECT_NOT_FOUND_ERROR_MESSAGE

logger = logging.getLogger(__name__)


class TenantService:
    _instance: Optional["TenantService"] = None
    _repository_instance: Optional[TenantRepository] = None

    def __init__(self, repository: TenantRepository, supabase_client: Optional[SupabaseClient] = None):
        self.repository = repository
        self.supabase_client = supabase_client

    async def get_users_statuses(self) -> List[TenantStatusDTO]:
        """
        Obtiene el nombre y estado de todos los usuarios basado en su actividad.
        - OK: Usuario logueado recientemente (último minuto).
        - WARNING: Usuario con correo confirmado pero no logueado recientemente.
        - ERROR: Usuario con correo no confirmado o inconsistencia de datos.
        """
        if not self.supabase_client:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Supabase client is not available."
            )

        try:
            response = self.supabase_client.rpc('get_all_user_details').execute()
            supabase_users_data = response.data
            
            supabase_status_map = {
                user['user_id']: {
                    'is_confirmed': user['is_confirmed'],
                    'last_sign_in_at': user['last_sign_in_at']
                }
                for user in supabase_users_data
            }

        except Exception as e:
            logger.error(f"Error calling RPC 'get_all_user_details': {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch user statuses from Supabase via RPC."
            )
        
        tenants = await self.repository.get_all()
        statuses = []
        
        # --- CAMBIO AQUÍ ---
        # Se define el umbral para considerar una sesión "activa" en 1 minuto.
        active_threshold = datetime.now(timezone.utc) - timedelta(minutes=1)

        for tenant in tenants:
            user_details = supabase_status_map.get(str(tenant.supabase_user_id))
            status_val = "ERROR"

            if user_details:
                if not user_details['is_confirmed']:
                    status_val = "ERROR"
                else:
                    last_sign_in_str = user_details.get('last_sign_in_at')
                    if last_sign_in_str:
                        try:
                            last_sign_in_dt = datetime.fromisoformat(last_sign_in_str)
                            if last_sign_in_dt > active_threshold:
                                status_val = "OK"
                            else:
                                status_val = "WARNING"
                        except (ValueError, TypeError):
                            status_val = "WARNING"
                    else:
                        status_val = "WARNING"

            statuses.append(TenantStatusDTO(name=tenant.name, status=status_val))
            
        return statuses

    async def create_tenant(self, new_tenant: TenantCreateDTO) -> TenantOutDTO:
        tenant_db_obj = Tenant(**new_tenant.model_dump())
        new_tenant_db_obj = await self.repository.create(new_tenant=tenant_db_obj)

        if not new_tenant_db_obj.id:
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE)

        return TenantOutDTO(**new_tenant_db_obj.model_dump())

    async def get_tenant_by_supabase_user_id(self, supabase_user_id: str) -> TenantOutDTO | None:
        tenant_db_obj = await self.repository.get_by_supabase_user_id(supabase_user_id=supabase_user_id)

        if not tenant_db_obj:
            raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)

        return TenantOutDTO(**tenant_db_obj.model_dump())

    async def get_all_tenants(self) -> list[TenantOutDTO]:
        tenants = await self.repository.get_all()
        return [TenantOutDTO(**tenant.model_dump()) for tenant in tenants]

    async def update_tenant(self, supabase_user_id: str, dto: TenantUpdateDTO) -> TenantOutDTO:
        tenant = await self.repository.get_by_supabase_user_id(supabase_user_id)
        if not tenant:
            raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)

        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tenant, key, value)

        updated = await self.repository.update(tenant)
        return TenantOutDTO(**updated.model_dump())

    async def delete_tenant(self, supabase_user_id: str):
        tenant = await self.repository.get_by_supabase_user_id(supabase_user_id)
        if not tenant:
            raise HTTPException(status_code=404, detail=OBJECT_NOT_FOUND_ERROR_MESSAGE)

        if self.supabase_client:
            try:
                response = self.supabase_client.rpc(
                    'delete_auth_user',
                    {'user_id': tenant.supabase_user_id}
                ).execute()

                if "Error" in response.data:
                    raise Exception(response.data)

                logger.info(f"User {tenant.supabase_user_id} deleted via RPC.")

            except Exception as e:
                logger.error(f"Error calling RPC to delete user from Supabase: {e}", exc_info=True)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not delete user via RPC.")

        await self.repository.delete(tenant)
        return {"message": "Tenant and associated user deleted"}
