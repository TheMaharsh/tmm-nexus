from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import AuthServiceDep, CurrentUser, DbSession, require_permission
from app.models.enums import Permission
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, RefreshRequest, TokenResponse, UserResponse
from app.schemas.common import ResponseBase
from app.schemas.dashboard import DashboardStatsResponse
from app.services.auth_service import build_user_response
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.post("/auth/login", response_model=ResponseBase[AuthResponse])
def login(payload: LoginRequest, auth_service: AuthServiceDep) -> ResponseBase[AuthResponse]:
    result = auth_service.login(payload.email, payload.password)
    return ResponseBase(data=result)


@router.post("/auth/refresh", response_model=ResponseBase[TokenResponse])
def refresh(payload: RefreshRequest, auth_service: AuthServiceDep) -> ResponseBase[TokenResponse]:
    tokens = auth_service.refresh(payload.refresh_token)
    return ResponseBase(data=tokens)


@router.post("/auth/logout", response_model=ResponseBase[None])
def logout(payload: RefreshRequest, auth_service: AuthServiceDep) -> ResponseBase[None]:
    auth_service.logout(payload.refresh_token)
    return ResponseBase(message="Logged out successfully")


@router.get("/auth/me", response_model=ResponseBase[UserResponse])
def me(user: CurrentUser) -> ResponseBase[UserResponse]:
    return ResponseBase(data=build_user_response(user))


@router.get("/dashboard/stats", response_model=ResponseBase[DashboardStatsResponse])
def dashboard_stats(
    db: DbSession,
    user: Annotated[User, Depends(require_permission(Permission.DASHBOARD_VIEW))],
) -> ResponseBase[DashboardStatsResponse]:
    service = DashboardService(db)
    stats = service.get_stats(user.organization_id)
    return ResponseBase(data=stats)
