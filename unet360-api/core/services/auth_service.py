from typing import Optional, Any
import logging
from fastapi import HTTPException, status 
from gotrue.errors import AuthApiError 
from supabase import Client as SupabaseClient 

from core.dtos.auth_dto import UserSignUpDTO, UserLoginDTO, AuthResponseDTO 
from core.services.tenant_service import TenantService 
from core.dtos.tenant_dto import TenantCreateDTO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) 


class AuthService:
    def __init__(self, supabase_client: SupabaseClient, tenant_service: TenantService):
        self.supabase_client = supabase_client
        self.tenant_service = tenant_service

    async def signup_user(self, user_data: UserSignUpDTO) -> dict:
        if not user_data.email.endswith('@unet.edu.ve'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration allowed only for '@unet.edu.ve' email addresses."
            )
        
        try:
            response_supabase = self.supabase_client.auth.sign_up(
                {
                    "email": user_data.email,
                    "password": user_data.password
                }
            )

            if response_supabase.user is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Supabase signup failed: Could not create user."
                )
            
            supabase_user_id = response_supabase.user.id

            tenant_create_dto_instance = TenantCreateDTO(
                name=user_data.email.split('@')[0],
                supabase_user_id=supabase_user_id,
                role="viewer" # Asignar un rol por defecto
            )
            
            await self.tenant_service.create_tenant(tenant_create_dto_instance)

            return {"message": "User successfully registered. Please check your email to confirm your account."}

        except AuthApiError as e:
            logger.error(f"AuthApiError during signup: {e.message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.message
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"An unexpected error occurred during signup in service: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )

    async def login_user(self, user_data: UserLoginDTO) -> AuthResponseDTO:
        try:
            response_supabase = self.supabase_client.auth.sign_in_with_password(
                {
                    "email": user_data.email,
                    "password": user_data.password
                }
            )

            if response_supabase.user is None or response_supabase.session is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Login failed: Invalid credentials or email not confirmed."
                )

            supabase_user_id = response_supabase.user.id
            access_token = response_supabase.session.access_token
            expires_in = response_supabase.session.expires_in

            tenant = await self.tenant_service.get_tenant_by_supabase_user_id(supabase_user_id)
            
            if not tenant:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User authenticated, but tenant profile not found in MongoDB."
                )

            auth_response = AuthResponseDTO(
                access_token=access_token,
                user_id=supabase_user_id,
                user_role=tenant.role,
                expires_in=expires_in
            )

            return auth_response

        except AuthApiError as e:
            logger.error(f"AuthApiError during login: {e.message}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e.message
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"An unexpected error occurred during login in service: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )

    async def logout_user(self, user_id: str):
        try:
            self.supabase_client.auth.sign_out() 
            
            logger.info(f"User {user_id} successfully logged out from Supabase.")
            
            return {"message": "User successfully logged out."}

        except AuthApiError as e:
            logger.error(f"AuthApiError during logout for user {user_id}: {e.message}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Logout failed: {e.message}"
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred during logout for user {user_id}: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )

