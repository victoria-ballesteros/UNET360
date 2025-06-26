from core.entities.node_model import Node

class NodeRepository:
    async def create(self, new_node: Node) -> Node | None:
        return await new_node.insert()
    
    async def get_by_name(self, name: str) -> Node | None:
        return await Node.find_one(Node.name == name)
    
    async def get_all(self) -> list[Node]:
        return await Node.find_all().to_list()
    
    async def update(self, node: Node) -> Node | None:
        return await node.save()
    
    async def delete(self, node: Node) -> None:
        await node.delete()
