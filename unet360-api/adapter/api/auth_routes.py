from fastapi import APIRouter, HTTPException, status, Request, Depends
import logging
from gotrue.errors import AuthApiError
import traceback

from core.dtos.responses_dto import GeneralResponse
# Se importa el nuevo DTO
from core.dtos.auth_dto import UserSignUpDTO, UserLoginDTO, AuthResponseDTO, ForgotPasswordDTO, ResetPasswordDTO
from core.services.tenant_service import TenantService
from adapter.database.tenant_repository import TenantRepository

from core.services.auth_service import AuthService

from supabase import Client as SupabaseClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

tenant_service = TenantService(TenantRepository())

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_auth_service(request: Request) -> AuthService:
    supabase_client_instance: SupabaseClient = request.app.state.supabase
    return AuthService(supabase_client_instance, tenant_service)


@router.post("/signup", response_model=GeneralResponse)
async def signup_user(user_data: UserSignUpDTO, 
                      auth_service: AuthService = Depends(get_auth_service)):
    try:
        signup_result = await auth_service.signup_user(user_data)
        
        return GeneralResponse(
            http_code=status.HTTP_201_CREATED,
            status=True,
            response_obj=signup_result
        )

    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during signup in route: {e}")
        traceback.print_exc()
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )


@router.post("/login", response_model=GeneralResponse)
async def login_user(user_data: UserLoginDTO, 
                     auth_service: AuthService = Depends(get_auth_service)):
    # ... código existente ...
    try:
        auth_response_dto = await auth_service.login_user(user_data)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=auth_response_dto.model_dump()
        )

    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during login in route: {e}")
        traceback.print_exc()
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.post("/forgot-password", response_model=GeneralResponse)
async def forgot_password(dto: ForgotPasswordDTO,
                          auth_service: AuthService = Depends(get_auth_service)):
    try:
        result = await auth_service.forgot_password(dto)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=result
        )

    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during forgot password in route: {e}")
        traceback.print_exc()
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

@router.post("/reset-password", response_model=GeneralResponse)
async def update_password(dto: ResetPasswordDTO,
                          auth_service: AuthService = Depends(get_auth_service)):
    try:
        result = await auth_service.reset_password(dto)
        return GeneralResponse(http_code=status.HTTP_200_OK, status=True, response_obj=result)
    except HTTPException as e:
        return GeneralResponse(http_code=e.status_code, status=False, response_obj={"message": e.detail})
    except Exception as e:
        return GeneralResponse(http_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status=False, response_obj={"message": str(e)})

@router.get("/status", response_model=GeneralResponse)
async def get_auth_status(request: Request):
    try:
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
                http_code=status.HTTP_200_OK,
                status=False,
                response_obj={
                    "is_authenticated": False,
                    "message": "User is not authenticated."
                }
            )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={
                "is_authenticated": False,
                "message": e.detail
            }
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred in auth status: {e}")
        traceback.print_exc()
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={
                "is_authenticated": False,
                "message": f"An unexpected error occurred: {str(e)}"
            }
        )


@router.post("/logout", response_model=GeneralResponse)
async def logout_user(request: Request,
                      auth_service: AuthService = Depends(get_auth_service)):
    # ... código existente ...
    try:
        user_id = getattr(request.state, "user_id", None)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated. Cannot log out."
            )
        
        logout_result = await auth_service.logout_user(user_id)
        
        return GeneralResponse(
            http_code=status.HTTP_200_OK,
            status=True,
            response_obj=logout_result
        )

    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during logout in route: {e}")
        traceback.print_exc()
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )