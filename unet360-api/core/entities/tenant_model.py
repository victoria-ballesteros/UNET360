from beanie import Document, Indexed
from pydantic import Field


class Tenant(Document):
    name: str
    supabase_user_id: Indexed(str, unique=True)
    role: str

    class Settings:
        name = "tentant"


