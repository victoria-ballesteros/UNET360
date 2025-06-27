from beanie import Document, Indexed
from typing import Optional

class Tag(Document):
    name: Indexed(str, unique=True)
    icon_name: Optional[str]

    class Settings:
        name = "tag"