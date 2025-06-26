from beanie import Document, Indexed

class Location(Document):
    name: Indexed(str, unique=True)

    class Settings:
        name = "location"