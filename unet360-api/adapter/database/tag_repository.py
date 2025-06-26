from core.entities.tag_model import Tag

class TagRepository:
    async def create(self, new_tag: Tag) -> Tag | None:
        return await new_tag.insert()
    
    async def get_by_name(self, name: str) -> Tag | None:
        return await Tag.find_one(Tag.name == name)
    
    async def get_all(self) -> list[Tag]:
        return await Tag.find_all().to_list()
    
    async def update(self, tag: Tag) -> Tag | None:
        return await tag.save()
    
    async def delete(self, tag: Tag) -> None:
        await tag.delete()
