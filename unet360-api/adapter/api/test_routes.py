from fastapi import APIRouter
from core.services.test_service import TestService
from adapter.database.test_repository import TestRepository
from core.dtos.test_dto import TestDTO

router = APIRouter(prefix="/tests", tags=["Tests"])
service = TestService(TestRepository())

@router.get("/")
async def get_tests():
    return {"message": "List of tests"}

@router.post("/")
async def create_test(test: TestDTO):
    created_test = await service.create_test(test)
    return {"message": "Test created", "test": created_test}
