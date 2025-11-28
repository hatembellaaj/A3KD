from datetime import datetime

from fastapi import FastAPI

app = FastAPI(title="A3KD Platform API", version="0.1.0")


@app.get("/")
def read_root():
    return {
        "message": "A3KD Platform API running",
        "docs_url": "/docs",
        "port": 8570,
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
