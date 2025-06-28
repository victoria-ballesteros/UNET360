# filename: general_response.py

from typing import Optional, Any
from pydantic import BaseModel, Field

class GeneralResponse(BaseModel):
    http_code: int
    status: bool
    response_obj: Optional[Any] = None

    @classmethod
    def success(cls, http_code: int, response_data: Optional[Any] = None) -> 'GeneralResponse':
        return cls(http_code=http_code, status=True, response_obj=response_data)

    @classmethod
    def error(cls, http_code: int, error_data: Optional[Any] = None) -> 'GeneralResponse':
        return cls(http_code=http_code, status=False, response_obj=error_data)