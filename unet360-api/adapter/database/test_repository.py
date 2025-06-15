from core.entities.test_model import Test

class TestRepository:
    async def create_test(self, new_test: Test) -> Test | None:
        return new_test.insert()