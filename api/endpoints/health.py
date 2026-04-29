from fastapi import APIRouter
from core.response import success_response
router = APIRouter()


@router.get("/")
def health_check():
    return success_response(status= "ok", message="API is healthy", data="")
