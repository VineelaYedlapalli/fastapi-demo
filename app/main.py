from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.routers import items, health     # ← add health

app = FastAPI(
    title="FastAPI Demo",
    description="Sprint Week 1 — Telusko Tutorial",
    version="0.4.0",
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


