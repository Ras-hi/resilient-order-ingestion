
from fastapi import FastAPI

app = FastAPI(title="OrderSync API")


@app.get("/")
def home():
    return {"message": "OrderSync is running"}

from app.source_api import router

app.include_router(router)
@app.get("/health")
def health():
    return {"status": "ok"}
    
from app.ingestion import ingest


@app.post("/ingestions/run")
def run_ingestion():
    return ingest()