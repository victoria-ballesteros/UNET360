import os
import zipfile

from fastapi import APIRouter, File, UploadFile, HTTPException, status, Request, Depends
from typing import Optional, Any
import logging
import traceback

from core.dtos.responses_dto import GeneralResponse

from supabase import Client as SupabaseClient

from core.services.local_upload_service import LocalUploadService
from core.services.upload_service import UploadService
from core.dependencies.auth_dependencies import get_current_admin_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/upload", tags=["Uploads"])

INTERNAL_BUCKET_PATH = os.getenv("INTERNAL_BUCKET_PATH")


def get_upload_service(request: Request) -> UploadService:
    supabase_client_instance: SupabaseClient = request.app.state.supabase
    return UploadService(supabase_client_instance)


@router.post("/image", response_model=GeneralResponse)
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    current_user_id: str = Depends(get_current_admin_user),
    upload_service: UploadService = Depends(get_upload_service),
):
    try:
        return GeneralResponse(
            http_code=status.HTTP_404_NOT_FOUND,
            status=True,
            response_obj={
                "message": "This endpoint is currently disabled for security reasons. Please contact support for assistance."
            },
        )

        upload_result = await upload_service.upload_image(
            file_content=await file.read(),
            file_name=file.filename,
            file_content_type=file.content_type,
            user_id=current_user_id,
        )

        return GeneralResponse(
            http_code=status.HTTP_201_CREATED, status=True, response_obj=upload_result
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code, status=False, response_obj={"message": e.detail}
        )
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during image upload in route: {e}",
            exc_info=True,
        )
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"},
        )


@router.delete("/image", response_model=GeneralResponse)
async def delete_image(
    request: Request,
    file_url: str,
    current_user_id: str = Depends(get_current_admin_user),
    upload_service: UploadService = Depends(get_upload_service),
):
    try:
        return GeneralResponse(
            http_code=status.HTTP_404_NOT_FOUND,
            status=True,
            response_obj={
                "message": "This endpoint is currently disabled for security reasons. Please contact support for assistance."
            },
        )

        delete_result = await upload_service.delete_image(
            file_name=file_url, user_id=current_user_id
        )

        return GeneralResponse(
            http_code=status.HTTP_200_OK, status=True, response_obj=delete_result
        )
    except HTTPException as e:
        return GeneralResponse(
            http_code=e.status_code, status=False, response_obj={"message": e.detail}
        )
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during image deletion in route: {e}",
            exc_info=True,
        )
        return GeneralResponse(
            http_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=False,
            response_obj={"message": f"An unexpected error occurred: {str(e)}"},
        )


@router.post("/tiles")
async def upload_tiles_folder(file: UploadFile = File(...)) -> GeneralResponse:
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files are accepted")

    file_content = await file.read()
    return await LocalUploadService().upload_image_tiles(
        file_content=file_content,
        file_name=file.filename.removesuffix(".zip"),
    )