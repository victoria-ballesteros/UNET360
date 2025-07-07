from fastapi import APIRouter, HTTPException, status, Request
import logging
from gotrue.errors import AuthApiError
import traceback

from core.dtos.responses_dto import GeneralResponse
from core.dtos.auth_dto import UserSignUpDTO, UserLoginDTO, AuthResponseDTO
from core.services.tenant_service import TenantService
from core.dtos.tenant_dto import TenantCreateDTO

from adapter.database.tenant_repository import TenantRepository


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

tenant_service = TenantService(TenantRepository())

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=GeneralResponse)
async def signup_user(user_data: UserSignUpDTO, request: Request):
    try:
        supabase_client = request.app.state.supabase

        if not user_data.email.endswith('@unet.edu.ve'):
            return GeneralResponse(
                http_code=status.HTTP_400_BAD_REQUEST,
                status=False,
                response_obj={"message": "Registration allowed only for '@unet.edu.ve' email addresses."}
            )
        
        response_supabase = supabase_client.auth.sign_up(
            {
                "email": user_data.email,
                "password": user_data.password
            }
        )

        if response_supabase.user is None:
            return GeneralResponse(
                http_code=status.HTTP_400_BAD_REQUEST,
                status=False,
                response_obj={"message": "Supabase signup failed: Could not create user."}
            )
        
        supabase_user_id = response_supabase.user.id

        tenant_create_dto_instance = TenantCreateDTO(
            name=user_data.email.split('@')[0],
            supabase_user_id=supabase_user_id,
            role="viewer"
        )
        
        await tenant_service.create_tenant(tenant_create_dto_instance)

        return GeneralResponse(
            http_code=status.HTTP_201_CREATED,
            status=True,
            response_obj={"message": "User successfully registered. Please check your email to confirm your account."}
        )

    except AuthApiError as e:
        return GeneralResponse(
            http_code=status.HTTP_400_BAD_REQUEST,
            status=False,
            response_obj={"message": e.message}
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during signup: {e}")
        traceback.print_exc()
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )


@router.post("/login", response_model=GeneralResponse)
async def login_user(user_data: UserLoginDTO, request: Request):
    try:
        supabase_client = request.app.state.supabase

        response_supabase = supabase_client.auth.sign_in_with_password(
            {
                "email": user_data.email,
                "password": user_data.password
            }
        )

        supabase_user_id = response_supabase.user.id
        access_token = response_supabase.session.access_token
        expires_in = response_supabase.session.expires_in

        tenant = await tenant_service.get_tenant_by_supabase_user_id(supabase_user_id)
        
        if not tenant:
            return GeneralResponse(
                http_code=status.HTTP_404_NOT_FOUND,
                status=False,
                response_obj={"message": "User authenticated, but tenant profile not found in MongoDB."}
            )

        auth_response = AuthResponseDTO(
            access_token=access_token,
            user_id=supabase_user_id,
            user_role=tenant.role,
            expires_in=expires_in
        )

        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=auth_response.model_dump()
        )

    except AuthApiError as e:
        return GeneralResponse(
            http_code=status.HTTP_401_UNAUTHORIZED,
            status=False,
            response_obj={"message": e.message}
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during login: {e}")
        traceback.print_exc()
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.get("/status", response_model=GeneralResponse)
async def get_auth_status(request: Request):
    """
    Endpoint para que el frontend verifique si el usuario está autenticado.
    Esta ruta está excluida del AuthMiddleware.
    """
    user_id = getattr(request.state, "user_id", None)
    user_role = getattr(request.state, "user_role", None)

    if user_id and user_role:
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj={
                "is_authenticated": True,
                "user_id": user_id,
                "user_role": user_role
            }
        )
    else:
        return GeneralResponse(
            http_code=status.HTTP_200_OK, # Se devuelve 200 OK porque la petición fue exitosa, solo que el usuario no está autenticado
            status=False, # Status False para indicar que la autenticación no está activa
            response_obj={
                "is_authenticated": False,
                "message": "User is not authenticated."
            }
        )
    
@router.post("/logout", response_model=GeneralResponse)
async def logout_user(request: Request):
    try:
        supabase_client = request.app.state.supabase
        
        user_id = getattr(request.state, "user_id", None)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated. Cannot log out."
            )
        response_supabase = supabase_client.auth.sign_out()
        
        logger.info(f"User {user_id} successfully logged out from Supabase.")
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj={"message": "User successfully logged out."}
        )

    except AuthApiError as e:
        logger.error(f"AuthApiError during logout for user {user_id}: {e.message}")
        return GeneralResponse(
            status=False,
            response_obj={"message": f"Logout failed: {e.message}"}
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during logout for user {user_id}: {e}")
        traceback.print_exc()
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )