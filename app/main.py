from fastapi import FastAPI

app = FastAPI(
    title="FastAPI Demo",
    description="Built following tutorial — Sprint Week 1",
    version="0.1.0",
)

@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "FastAPI is live"}