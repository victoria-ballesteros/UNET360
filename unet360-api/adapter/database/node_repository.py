from core.entities.node_model import Node

class NodeRepository:
    # Inserta un nuevo nodo en la base de datos
    async def create(self, new_node: Node) -> Node | None:
        return await new_node.insert()
    
    async def get_by_name(self, name: str) -> Node | None:
        return await Node.find_one(Node.name == name)
    
    async def get_all(self) -> list[Node]:
        return await Node.find_all().to_list()
    
    async def get_paginated(self, skip: int, limit: int, search: str = None) -> tuple[list[Node], int]:
        if search:
            query = Node.find(Node.name == {"$regex": search, "$options": "i"})
        else:
            query = Node.find_all()
        total = await query.count()
        items = await query.sort("name").skip(skip).limit(limit).to_list()
        return items, total
    
    async def get_keyset_paginated(self, page: int, page_size: int, sort: str = "asc", search: str = None) -> tuple[list[Node], int]:
        # 1. Obtener conteo total con una consulta fresca
        count_query = Node.find_all()
        if search:
            count_query = count_query.find(Node.name == {"$regex": search, "$options": "i"})
        total = await count_query.count()
        
        sort_param = "+name" if sort == "asc" else "-name"
        
        if page <= 1:
            # Página 1: Consulta limpia sin saltos (skip)
            items_query = Node.find_all()
            if search:
                items_query = items_query.find(Node.name == {"$regex": search, "$options": "i"})
            items = await items_query.sort(sort_param).limit(page_size).to_list()
        else:
            # Páginas intermedias/finales: Consulta limpia para buscar la frontera
            boundary_query = Node.find_all()
            if search:
                boundary_query = boundary_query.find(Node.name == {"$regex": search, "$options": "i"})
            
            skip_count = (page - 1) * page_size
            boundary_nodes = await boundary_query.sort(sort_param).skip(skip_count - 1).limit(1).to_list()
            
            if boundary_nodes:
                cursor_name = boundary_nodes[0].name
                
                # Consulta limpia para obtener los items reales de la página
                items_query = Node.find_all()
                if search:
                    items_query = items_query.find(Node.name == {"$regex": search, "$options": "i"})
                
                if sort == "asc":
                    items_query = items_query.find(Node.name > cursor_name)
                else:
                    items_query = items_query.find(Node.name < cursor_name)
                
                items = await items_query.sort(sort_param).limit(page_size).to_list()
            else:
                items = []
        return items, total
    
    async def update(self, node: Node) -> Node | None:
        return await node.save()
    
    async def delete(self, node: Node) -> None:
        await node.delete()
