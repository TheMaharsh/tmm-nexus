from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class RoleResponse(BaseModel):
    id: str
    name: str
    permissions: list[str]

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    organization_id: str
    organization_name: str
    role: RoleResponse

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    user: UserResponse
    tokens: TokenResponse
