from core.entities.tenant_model import Tenant


class TenantRepository:
    # Inserta un nuevo tenant en la base de datos
    async def create(self, new_tenant: Tenant) -> Tenant | None:
        return await new_tenant.insert()

    async def get_by_name(self, name: str) -> Tenant | None:
        return await Tenant.find_one(Tenant.name == name)

    async def get_by_supabase_user_id(self, supabase_user_id: str) -> Tenant | None:
        return await Tenant.find_one(Tenant.supabase_user_id == supabase_user_id)

    async def get_all(self) -> list[Tenant]:
        return await Tenant.find_all().to_list()

    async def get_keyset_paginated(self, page: int, page_size: int, sort: str = "asc", search: str = None) -> tuple[list[Tenant], int]:
        count_query = Tenant.find_all()
        if search:
            count_query = count_query.find(Tenant.name == {"$regex": search, "$options": "i"})
        total = await count_query.count()
        
        sort_param = "+name" if sort == "asc" else "-name"
        
        if page <= 1:
            items_query = Tenant.find_all()
            if search:
                items_query = items_query.find(Tenant.name == {"$regex": search, "$options": "i"})
            items = await items_query.sort(sort_param).limit(page_size).to_list()
        else:
            boundary_query = Tenant.find_all()
            if search:
                boundary_query = boundary_query.find(Tenant.name == {"$regex": search, "$options": "i"})
            
            skip_count = (page - 1) * page_size
            boundary_tenants = await boundary_query.sort(sort_param).skip(skip_count - 1).limit(1).to_list()
            
            if boundary_tenants:
                cursor_name = boundary_tenants[0].name
                
                items_query = Tenant.find_all()
                if search:
                    items_query = items_query.find(Tenant.name == {"$regex": search, "$options": "i"})
                
                if sort == "asc":
                    items_query = items_query.find(Tenant.name > cursor_name)
                else:
                    items_query = items_query.find(Tenant.name < cursor_name)
                
                items = await items_query.sort(sort_param).limit(page_size).to_list()
            else:
                items = []
        return items, total

    async def update(self, tenant: Tenant) -> Tenant | None:
        return await tenant.save()

    async def delete(self, tenant: Tenant) -> None:
        await tenant.delete()