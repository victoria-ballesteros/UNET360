import os
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from supabase import create_client
from core.entities.test_model import Test
from .test_routes import router as test_router


load_dotenv()
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = None

    try: 
        # Initialize MongoDB connection
        mongo_db = os.getenv("MONGODB_DB")
        mongo_uri = os.getenv("MONGODB_URL")
        supabase_uri = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY") 
        client = AsyncIOMotorClient(mongo_uri, authSource="admin")

        await init_beanie(
            database=client[mongo_db],
            document_models=[
                Test
            ]
        )

        # Supabase client
        supabase = create_client(supabase_uri, supabase_key)
        app.state.supabase = supabase

        yield
    finally:
        # Cleanup (if needed)
        if client is not None:
            client.close()

app = FastAPI(title="UNET360 API", lifespan=lifespan)
app.include_router(test_router)

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
    return {"message": "UNET360 API is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
