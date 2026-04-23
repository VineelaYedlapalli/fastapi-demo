from fastapi import FastAPI
from app.routers import items

app = FastAPI(
    title="FastAPI Demo",
    description="Built following tutorial - Sprint week 1",
    version="0.2.0",
)

app.include_router(items.router)

@app.get("/",tags=["Health"])
def root():
    return {"status":"ok","message":"FastAPI is live"}