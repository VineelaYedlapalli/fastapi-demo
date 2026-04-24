from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import items

app = FastAPI(
    title="FastAPI Demo",
    description="Sprint Week 1 — Telusko Tutorial",
    version="0.3.0",
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    All HTTPExceptions (404, 400, etc.) return a consistent JSON shape.
    Without this, FastAPI returns different formats in different situations.
    """
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
    """
    Pydantic validation failures (wrong type, missing required field)
    return a clean 422 with human-readable errors.
    """
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "status_code": 422,
            "message": "Validation error — check your request body",
            "errors": exc.errors(),
        },
    )


# Routers
app.include_router(items.router)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "FastAPI is live"}