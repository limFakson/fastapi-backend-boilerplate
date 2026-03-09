from fastapi import FastAPI
from api.router import api_router

app = FastAPI(
    title="Fastapi Backend",
    description="Starter boilerplate for scalable FastAPI backend",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Backend running"}
