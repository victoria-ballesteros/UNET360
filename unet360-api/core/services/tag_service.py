from typing import Optional
from fastapi import HTTPException

from adapter.database.tag_repository import TagRepository
from core.dtos.tag_dto import TagCreateDTO, TagUpdateDTO, TagOutDTO
from core.entities.tag_model import Tag
from core.messages.error_messages import CREATE_ERROR_MESSAGE


class TagService:
    _instance: Optional["TagService"] = None
    _repository_instance: Optional[TagRepository] = None

    def __init__(self, repository: TagRepository):
        self.repository = repository

    async def create_tag(self, new_tag: TagCreateDTO) -> TagCreateDTO | None:
        tag_db_obj = Tag(**{**new_tag.dict(exclude_none=True)})
        new_tag_db_obj = await self.repository.create(new_tag=tag_db_obj)

        if not new_tag_db_obj.id:
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE)

        return TagCreateDTO(**new_tag_db_obj.dict())

    async def get_tag_by_name(self, name: str) -> TagOutDTO | None:
        tag_db_obj = await self.repository.get_by_name(name=name)

        if not tag_db_obj:
            raise HTTPException(status_code=404, detail="tag not found")

        return TagOutDTO(**tag_db_obj.dict())

    async def get_all_tags(self) -> list[TagOutDTO]:
        tags = await self.repository.get_all()
        return [TagOutDTO(**tag.dict()) for tag in tags]

    async def update_tag(self, name: str, dto: TagUpdateDTO) -> TagOutDTO:
        tag = await self.repository.get_by_name(name)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")

        update_data = dto.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(tag, key, value)

        updated = await self.repository.update(tag)
        return TagOutDTO(**updated.dict())

    async def delete_tag(self, name: str):
        tag = await self.repository.get_by_name(name)
        if not tag:
            raise HTTPException(status_code=404, detail="Tag not found")
        await self.repository.delete(tag)
        return {"message": "Tag deleted"}
