from typing import Optional
from fastapi import HTTPException

from adapter.database.test_repository import TestRepository
from core.dtos.test_dto import TestDTO
from core.entities.test_model import Test
from core.messages.error_messages import CREATE_ERROR_MESSAGE

class TestService:
    _instance: Optional["TestService"] = None
    _repository_instance: Optional[TestRepository] = None

    def __init__(self, repository: TestRepository):
        self.repository = repository

    async def create_test(self, new_test: TestDTO) -> TestDTO | None:
        test_db_obj = Test(**{**new_test.dict(exclude_none=True)})
        new_test_db_obj = await self.repository.create_test(new_test=test_db_obj)

        if not new_test_db_obj.id:
            raise HTTPException(status_code=500, detail=CREATE_ERROR_MESSAGE)

        return TestDTO(**new_test_db_obj.dict())