from fastapi.responses import JSONResponse
from typing import Any, Optional
from pydantic import BaseModel


def _serialize_data(data: Any) -> Any:
    """Convert common objects to JSON serializable structures."""
    if isinstance(data, BaseModel):
        return data.dict()

    if isinstance(data, dict):
        return {k: _serialize_data(v) for k, v in data.items()}

    if isinstance(data, list):
        return [_serialize_data(v) for v in data]

    if hasattr(data, "dict") and callable(getattr(data, "dict")):
        try:
            return data.dict()
        except Exception:
            pass

    if isinstance(data, (str, int, float, bool)) or data is None:
        return data

    # UUID objects are common in SQLAlchemy models and pydantic ids
    try:
        import uuid

        if isinstance(data, uuid.UUID):
            return str(data)
    except ImportError:
        pass

    if hasattr(data, "__dict__"):
        obj_dict = {
            k: _serialize_data(v)
            for k, v in data.__dict__.items()
            if not k.startswith("_") and k != "hashed_password"
        }
        # Remove SQLAlchemy internal state if present
        obj_dict.pop("_sa_instance_state", None)
        return obj_dict

    return str(data)


def success_response(data: Any, message: str = "Success", status: int = 200):
    return JSONResponse(
        status_code=status,
        content={
            "success": True,
            "status": status,
            "message": message,
            "data": _serialize_data(data),
        },
    )


def error_response(status: int, message: str, details: Optional[Any] = None):
    return JSONResponse(
        status_code=status,
        content={
            "success": False,
            "status": status,
            "message": message,
            "details": _serialize_data(details),
        },
    )
