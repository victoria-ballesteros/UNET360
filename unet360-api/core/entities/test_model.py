from beanie import Document

class Test(Document):
    url: str

    class Settings:
        name = "test"