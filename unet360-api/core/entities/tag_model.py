from beanie import Document

class Tag(Document):
    name: str
    icon_name: str

    class Settings:
        name = "tag"