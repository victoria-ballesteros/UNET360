from pydantic import BaseModel, Field
from typing import Optional

class UserSignUpDTO(BaseModel):
    email: str
    password: str

class UserLoginDTO(BaseModel):
    email: str
    password: str

class AuthResponseDTO(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    user_role: Optional[str] = None
    expires_in: Optional[int] = None

class ForgotPasswordDTO(BaseModel):
    email: str

class ResetPasswordDTO(BaseModel):
    access_token: str
    refresh_token: str
    new_password: str
