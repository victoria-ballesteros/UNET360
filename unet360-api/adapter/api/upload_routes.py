from fastapi import APIRouter, File, UploadFile, HTTPException, status, Request, Depends
from typing import Optional, Any
import logging

from core.dtos.responses_dto import GeneralResponse

from supabase import Client as SupabaseClient

from core.services.upload_service import UploadService
from core.dependencies.auth_dependencies import get_current_admin_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/upload", tags=["Uploads"])

def get_upload_service(request: Request) -> UploadService:
    supabase_client_instance: SupabaseClient = request.app.state.supabase
    return UploadService(supabase_client_instance)


@router.post("/image", response_model=GeneralResponse)
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    current_user_id: str = Depends(get_current_admin_user),
    upload_service: UploadService = Depends(get_upload_service)
):
    try: 
        upload_result = await upload_service.upload_image(
            file_content=await file.read(),
            file_name=file.filename,
            file_content_type=file.content_type,
            user_id=current_user_id
        )
        
        return GeneralResponse(
            http_code=status.HTTP_201_CREATED,
            status=True,
            response_obj=upload_result
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during image upload in route: {e}", exc_info=True)
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

