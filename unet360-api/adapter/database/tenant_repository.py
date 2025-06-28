from core.entities.tenant_model import Tenant


class TenantRepository:
    # Inserta un nuevo tenant en la base de datos
    async def create(self, new_tenant: Tenant) -> Tenant | None:
        return await new_tenant.insert()

    async def get_by_supabase_user_id(self, supabase_user_id: str) -> Tenant | None:
        return await Tenant.find_one(Tenant.supabase_user_id == supabase_user_id)

    async def get_all(self) -> list[Tenant]:
        return await Tenant.find_all().to_list()

    async def update(self, tenant: Tenant) -> Tenant | None:
        return await tenant.save()

    async def delete(self, tenant: Tenant) -> None:
        await tenant.delete()