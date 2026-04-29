from fastapi import FastAPI, Request
from api.router import api_router
from core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import OperationalError
from fastapi.responses import FileResponse, JSONResponse
from core.response import error_response, success_response
from constants import status_codes
import logging

app = FastAPI(
    title="Fastapi Backend",
    description="Starter boilerplate for scalable FastAPI backend",
    version="1.0.0",
)

# Set CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Backend running"}


@app.middleware("http")
async def response_wrapper_middleware(request: Request, call_next):
    """Auto-wrap successful JSON responses that aren't already wrapped"""
    if not settings.ENABLE_RESPONSE_AUTO_WRAP:
        return await call_next(request)

    # Do not wrap OpenAPI / docs endpoints, Swagger UI requests, or static files
    if request.url.path in [
        settings.API_V1_STR + "/openapi.json",
        "/openapi.json",
        "/docs",
        "/redoc",
    ]:
        return await call_next(request)

    response = await call_next(request)

    # Skip wrapping for non-JSON responses, file responses, or already-wrapped responses
    if response.status_code < 300 and "application/json" in response.headers.get(
        "content-type", ""
    ):
        try:
            import json

            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            data = json.loads(body)

            # Check if already wrapped (has success, status, message keys)
            if not all(key in data for key in ["success", "status", "message"]):
                # Auto-wrap the response
                wrapped = success_response(
                    data=data, message=request.url.path, status=response.status_code
                )
                return wrapped
            else:
                # Already wrapped, return as-is
                return JSONResponse(
                    content=data,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )
        except Exception:
            # If parsing fails, return original response
            return response

    return response


app.include_router(api_router, prefix=settings.API_V1_STR)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return error_response(status=exc.status_code, message=str(exc.detail), details=None)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [
        {"loc": loc, "msg": err["msg"], "type": err["type"]}
        for err in exc.errors()
        for loc in ["->".join([str(p) for p in err["loc"]])]
    ]
    return error_response(
        status=status_codes.UNPROCESSABLE_ENTITY,
        message="Validation error",
        details=details,
    )


@app.exception_handler(OperationalError)
async def operational_exception_handler(request: Request, exc: OperationalError):
    logging.exception("Database operational error")
    # engine.dispose()
    return error_response(
        status=status_codes.SERVICE_UNAVAILABLE,
        message="Database temporarily unavailable",
        details=str(exc),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.exception("Unhandled exception")
    return error_response(
        status=status_codes.INTERNAL_SERVER_ERROR,
        message="Internal server error",
        details=str(exc),
    )

