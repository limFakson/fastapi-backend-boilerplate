"""Response schema models for API documentation and type safety"""
from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, Any

from constants import status_codes

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standardized success response wrapper"""
    success: bool = True
    status: int
    message: str
    data: Optional[T] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "status": status_codes.SUCCESS,
                "message": "Success",
                "data": {},
            }
        }


class PaginatedData(BaseModel, Generic[T]):
    total: int
    page: int
    limit: int
    totalPages: int
    data: list[T]


class ErrorResponse(BaseModel):
    """Standardized error response wrapper"""
    success: bool = False
    status: int
    message: str
    details: Optional[Any] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "status": status_codes.BAD_REQUEST,
                "message": "Bad Request",
                "details": None,
            }
        }
