from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response, JSONResponse # <-- Importa JSONResponse
from starlette.types import ASGIApp
import logging

from supabase import Client as SupabaseClient

from core.services.tenant_service import TenantService
from adapter.database.tenant_repository import TenantRepository
from core.dtos.responses_dto import GeneralResponse 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.tenant_service = TenantService(TenantRepository())
        
        self.excluded_paths = [
            "/",
            "/auth/signup/",
            "/auth/login/",
            "/auth/status/",
            "/docs",
            "/redoc",       
            "/openapi.json",
        ]

    async def dispatch(self, request: Request, call_next):
        # Si la ruta está excluida, simplemente la pasa
        if request.url.path == "/auth/status":
            try:
                auth_header = request.headers.get("Authorization")
                if auth_header and auth_header.startswith("Bearer "):
                    access_token = auth_header.split(" ", 1)[1]
                    supabase_client: SupabaseClient = request.app.state.supabase
                    user_response = supabase_client.auth.get_user(access_token)
                    
                    if user_response.user is not None:
                        request.state.user_id = user_response.user.id
                        tenant_profile = await self.tenant_service.get_tenant_by_supabase_user_id(request.state.user_id)
                        request.state.user_role = tenant_profile.role if tenant_profile else None
                        logger.info(f"Auth status check: User {request.state.user_id} authenticated.")
            except Exception as e:
                logger.warning(f"Auth status check failed: {e}")
            return await call_next(request)

        if request.url.path in self.excluded_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=GeneralResponse(
                    http_code=status.HTTP_401_UNAUTHORIZED,
                    status=False,
                    response_obj={"message": "Authorization header missing"}
                ).model_dump()
            )

        token_type, access_token = None, None
        if auth_header.startswith("Bearer "):
            try:
                token_type, access_token = auth_header.split(" ", 1)
            except ValueError:
                # --- CAMBIO AQUI: Devolver JSONResponse directamente ---
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content=GeneralResponse(
                        http_code=status.HTTP_401_UNAUTHORIZED,
                        status=False,
                        response_obj={"message": "Invalid Authorization header format. Expected 'Bearer <token>'."}
                    ).model_dump()
                )
        
        if token_type != "Bearer" or not access_token:
            # --- CAMBIO AQUI: Devolver JSONResponse directamente ---
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=GeneralResponse(
                    http_code=status.HTTP_401_UNAUTHORIZED,
                    status=False,
                    response_obj={"message": "Invalid token type. Expected 'Bearer'."}
                ).model_dump()
            )

        supabase_client: SupabaseClient = request.app.state.supabase
        user_id = None
        user_role = None

        try:
            user_response = supabase_client.auth.get_user(access_token) 
            
            if user_response.user is None:
                # --- CAMBIO AQUI: Devolver JSONResponse directamente ---
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content=GeneralResponse(
                        http_code=status.HTTP_401_UNAUTHORIZED,
                        status=False,
                        response_obj={"message": "Invalid or expired token. User not found in Supabase."}
                    ).model_dump()
                )
            
            user_id = user_response.user.id

            tenant_profile = await self.tenant_service.get_tenant_by_supabase_user_id(user_id)
            
            if not tenant_profile:
                # --- CAMBIO AQUI: Devolver JSONResponse directamente ---
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content=GeneralResponse(
                        http_code=status.HTTP_403_FORBIDDEN,
                        status=False,
                        response_obj={"message": "User profile not found in application database. Access denied."}
                    ).model_dump()
                )
            
            user_role = tenant_profile.role

            request.state.user_id = user_id
            request.state.user_role = user_role
            logger.info(f"Authenticated user: {user_id} with role: {user_role}")

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, # O 500, pero 401 es más apropiado para fallos de auth
                content=GeneralResponse(
                    http_code=status.HTTP_401_UNAUTHORIZED,
                    status=False,
                    response_obj={"message": f"Authentication failed: {str(e)}"}
                ).model_dump()
            )

        response = await call_next(request)
        return response

