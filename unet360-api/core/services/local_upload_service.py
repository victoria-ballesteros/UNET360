import os
import zipfile
import logging

from fastapi import HTTPException, status # type: ignore

from core.dtos.responses_dto import GeneralResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LocalUploadService:
    def __init__(self) -> None:
        self.internal_bucket_path = os.getenv("INTERNAL_BUCKET_PATH")

    async def upload_image_tiles(
        self, file_content: bytes, file_name: str
    ) -> GeneralResponse:
        if not self.internal_bucket_path or not os.path.exists(
            self.internal_bucket_path
        ):
            raise HTTPException(
                status_code=500,
                detail="Internal bucket path not configured or not found",
            )

        temp_zip_path = os.path.join(self.internal_bucket_path, f"{file_name}.zip")

        try:
            with open(temp_zip_path, "wb") as buffer:
                buffer.write(file_content)

            with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
                for zip_info in zip_ref.infolist():
                    target_path = os.path.realpath(
                        os.path.join(self.internal_bucket_path, zip_info.filename)
                    )
                    if not target_path.startswith(
                        os.path.realpath(self.internal_bucket_path)
                    ):
                        raise HTTPException(
                            status_code=400, detail="Invalid path in ZIP file"
                        )
                    zip_ref.extract(zip_info, self.internal_bucket_path)

                image_folder = zip_ref.namelist()[0].split("/")[0]

            return GeneralResponse(
                http_code=status.HTTP_200_OK,
                status=True,
                response_obj={
                    "message": "Tiles uploaded successfully",
                    "image_folder": image_folder,
                    "destination": os.path.join(
                        self.internal_bucket_path, image_folder
                    ),
                },
            )

        except zipfile.BadZipFile:
            raise HTTPException(
                status_code=400, detail="Uploaded file is not a valid ZIP"
            )

        except HTTPException:
            raise

        except Exception as e:
            logger.error(f"Upload failed: {e}")
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

        finally:
            if os.path.exists(temp_zip_path):
                os.remove(temp_zip_path)
