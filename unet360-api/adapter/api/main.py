import os
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from supabase import create_client
from core.entities.location_model import Location
from core.entities.tag_model import Tag
from core.entities.node_model import Node
from core.entities.tenant_model import Tenant


from .location_routes import router as location_router
from .tag_routes import router as tag_router
from .node_routes import router as node_router    
from .tenant_routes import router as tenant_router     
from .graph_routes import router as graph_router         


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
                Location,
                Tag,
                Node,
                Tenant
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

routers = [
    location_router,
    tag_router,
    node_router,
    tenant_router,
    graph_router
]

app = FastAPI(title="UNET360 API", lifespan=lifespan)
for router in routers:
    app.include_router(router)

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
