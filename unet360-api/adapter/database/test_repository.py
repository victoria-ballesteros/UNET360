from core.entities.test_model import Test


class TestRepository:
    # Inserta un nuevo test en la base de datos
    async def create_test(self, new_test: Test) -> Test | None:
        return await new_test.insert()