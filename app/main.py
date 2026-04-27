from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.routers import items, health
from app.config import settings
from app.logger import logger


# ── API Metadata ────────────────────────────────────────────────────────────
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


# ── CORS Middleware ─────────────────────────────────────────────────────────
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Logging Middleware (NEW) ────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"Response status: {response.status_code}")

    return response


# ── Exception Handlers (WITH LOGGING) ───────────────────────────────────────
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP error: {exc.detail} | Status: {exc.status_code}")
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
    logger.error(f"Validation error: {exc.errors()}")
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