import os
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from core.entities.node import Node


load_dotenv()
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = None

    try: 
        # Initialize MongoDB connection
        mongo_db = os.getenv("MONGODB_DB", "catalogs_db")
        mongo_uri = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
        logger.debug('MONGODB_URL' + mongo_uri)
        logger.debug('MONGODB_DB' + mongo_db)
        client = AsyncIOMotorClient(mongo_uri, authSource=mongo_db)

        await init_beanie(
            database=client[os.getenv("MONGODB_DB", "catalogs_db")],
            document_models=[
                Node
            ]
        )
        yield
    finally:
        # Cleanup (if needed)
        if client is not None:
            client.close()

app = FastAPI(title="TC4 Catalogs API", lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "TC4 Catalogs API is running. Visit /graphql for the GraphQL playground"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
