from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    success: bool = True
    data: T | None = None
    message: str | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: Any | None = None


class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: list[T]
    meta: PaginationMeta
