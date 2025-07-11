from fastapi import APIRouter, File, UploadFile, HTTPException, status, Request, Depends
from typing import Optional, Any
import logging

from core.dtos.responses_dto import GeneralResponse

from supabase import Client as SupabaseClient
from storage3.exceptions import StorageApiError 

from core.dependencies.auth_dependencies import get_current_admin_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/upload", tags=["Uploads"])

SUPABASE_BUCKET_NAME = "virtual-environment-images"


@router.post("/image", response_model=GeneralResponse)
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    current_user_id: str = Depends(get_current_admin_user)
):
    try: 
        supabase_client: SupabaseClient = request.app.state.supabase
        
        if not file.content_type.startswith("image/"):
            return GeneralResponse(
                http_code=status.HTTP_400_BAD_REQUEST,
                status=False,
                response_obj={"message": "Invalid file type. Only image files are allowed."}
            )

        contents = await file.read()
        
        file_path_in_bucket = f"{file.filename}" 
        response_storage = supabase_client.storage.from_(SUPABASE_BUCKET_NAME).upload(
            file_path_in_bucket,
            contents,
            {"content-type": file.content_type}
        )
        uploaded_file_path_from_supabase = response_storage.path 
        signed_url_response = supabase_client.storage.from_(SUPABASE_BUCKET_NAME).create_signed_url(
            file.filename,
            60 
        )
        signed_url = signed_url_response.data.signedUrl if signed_url_response.data else None

        return GeneralResponse(
            http_code=status.HTTP_201_CREATED,
            status=True,
            response_obj={
                "message": "Image uploaded successfully to private bucket.",
                "file_path": uploaded_file_path_from_supabase, 
                "signed_url": signed_url
            }
        )
    except StorageApiError as e:
        logger.error(f"Supabase Storage API error during image upload: {e}", exc_info=True)
        error_detail = e.message if hasattr(e, 'message') else str(e)
        status_code_from_api = e.status_code if hasattr(e, 'status_code') else status.HTTP_500_INTERNAL_SERVER_ERROR
        return GeneralResponse(
            http_code=status_code_from_api,
            status=False,
            response_obj={"message": f"Supabase Storage upload failed: {error_detail}"}
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code,
            status=False,
            response_obj={"message": e.detail}
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during image upload: {e}", exc_info=True)
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"}
        )

