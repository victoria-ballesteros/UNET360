from beanie import Document
from pydantic import ConfigDict


class Node(Document):
    url: str

    model_config = ConfigDict(collection_name="node")