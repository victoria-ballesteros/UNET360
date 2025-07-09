from fastapi import APIRouter, File, UploadFile, HTTPException, status, Request, Depends
from typing import Optional, Any
import logging

from core.dtos.responses_dto import GeneralResponse

from supabase import Client as SupabaseClient

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
        
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "png"
        file_path_in_bucket = f"{current_user_id}/{file.filename}" 
        
        response_storage = supabase_client.storage.from_(SUPABASE_BUCKET_NAME).upload(
            file_path_in_bucket,
            contents,
            {"content-type": file.content_type}
        )

        if response_storage.status_code == 200:
            signed_url_response = supabase_client.storage.from_(SUPABASE_BUCKET_NAME).create_signed_url(
                file_path_in_bucket,
                60
            )
            
            signed_url = signed_url_response.data.signedUrl if signed_url_response.data else None

            return GeneralResponse(
                http_code=status.HTTP_201_CREATED,
                status=True,
                response_obj={
                    "message": "Image uploaded successfully to private bucket.",
                    "file_path": file_path_in_bucket,
                    "signed_url": signed_url
                }
            )
        else:
            error_message = f"Supabase Storage upload failed: {response_storage.json()}"
            return GeneralResponse(
                http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status=False,
                response_obj={"message": error_message}
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

