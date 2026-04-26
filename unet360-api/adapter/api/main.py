import logging
import os
from contextlib import asynccontextmanager

import uvicorn
from adapter.api.auth_routes import router as auth_router
from adapter.api.graph_routes import router as graph_router
from adapter.api.location_routes import router as location_router
from adapter.api.node_routes import router as node_router
from adapter.api.tag_routes import router as tag_router
from adapter.api.tenant_routes import router as tenant_router
from adapter.api.upload_routes import router as upload_router
from adapter.external.supabase_adapter import create_supabase_client
from beanie import init_beanie
from core.dtos.responses_dto import GeneralResponse
from core.entities.location_model import Location
from core.entities.node_model import Node
from core.entities.tag_model import Tag
from core.entities.tenant_model import Tenant
from core.middleware.auth_middleware import AuthMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import AsyncMongoClient

load_dotenv()
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = None

    try:
        mongo_db_name = os.getenv("MONGODB_DB")
        mongo_uri = os.getenv("MONGODB_URL")

        client = AsyncMongoClient(mongo_uri)
        database = client.get_database(mongo_db_name)

        await init_beanie(
            database=database, document_models=[Location, Tag, Node, Tenant]
        )

        supabase = create_supabase_client()
        app.state.supabase = supabase

        yield
    finally:
        if client is not None:
            await client.close()


routers = [
    location_router,
    tag_router,
    node_router,
    tenant_router,
    graph_router,
    auth_router,
    upload_router,
]

app = FastAPI(title="UNET360 API", lifespan=lifespan)

app.add_middleware(AuthMiddleware)

for router_instance in routers:
    app.include_router(router_instance)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    response_content = GeneralResponse(
        http_code=exc.status_code, status=False, response_obj={"message": exc.detail}
    )
    return JSONResponse(
        status_code=exc.status_code, content=response_content.model_dump()
    )


@app.get("/")
async def root():
    return {"message": "UNET360 API is running."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
