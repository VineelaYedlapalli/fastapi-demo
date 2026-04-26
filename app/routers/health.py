from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
def root():
    return {
        "status": "ok",
        "message": "FastAPI is live",
        "version": "0.4.0"
    }