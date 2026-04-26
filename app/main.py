from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import items, health
from app.config import settings

tags_metadata = [
    {
        "name": "Health",
        "description": "Health check endpoint to verify the API is running.",
    },
    {
        "name": "Items",
        "description": "CRUD operations for managing items in the store.",
    },
]

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A production-ready REST API built with FastAPI during Sprint Week 1.",
    contact={"name": "Vineela Yedlapalli", "email": "vineelayedlapalli@gmail.com"},
    openapi_tags=tags_metadata,
)


# ── Exception handlers ─────────────────────────────────────────────────────
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "status_code": 422,
            "message": "Validation error — check your request body",
            "errors": exc.errors(),
        },
    )


# ── Routers ────────────────────────────────────────────────────────────────

app.include_router(health.router)    
app.include_router(items.router)


