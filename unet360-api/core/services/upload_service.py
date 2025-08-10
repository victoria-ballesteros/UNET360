from typing import Optional, Any
import logging

from fastapi import HTTPException, status
from supabase import Client as SupabaseClient
from storage3.exceptions import StorageApiError

from core.dtos.responses_dto import GeneralResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class UploadService:
    def __init__(self, supabase_client: SupabaseClient):
        self.supabase_client = supabase_client
        self.supabase_bucket_name = "virtual-environment-images"

    async def upload_image(self, file_content: bytes, file_name: str, file_content_type: str, user_id: str) -> dict:
        try:
            file_path_in_bucket = f"{file_name}"

            response_storage = self.supabase_client.storage.from_(self.supabase_bucket_name).upload(
                file_path_in_bucket,
                file_content,
                {"content-type": file_content_type}
            )

            public_url_response = self.supabase_client.storage.from_(self.supabase_bucket_name).get_public_url(file_path_in_bucket)
            uploaded_file_path_from_supabase = response_storage.full_path

            return {
                "message": "Image uploaded successfully to private bucket.",
                "file_path": uploaded_file_path_from_supabase,
                "signed_url": public_url_response
            }
        except StorageApiError as e:
            logger.error(f"Supabase Storage API error during image upload: {e}", exc_info=True)
            error_detail = e.message if hasattr(e, 'message') else str(e)
            status_code_from_api = e.status_code if hasattr(e, 'status_code') else status.HTTP_500_INTERNAL_SERVER_ERROR
            raise HTTPException(
                status_code=status_code_from_api,
                detail=f"Supabase Storage upload failed: {error_detail}"
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred during image upload: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )
