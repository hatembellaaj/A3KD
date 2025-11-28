from __future__ import annotations

from datetime import datetime
from threading import Lock
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator

app = FastAPI(title="A3KD Platform API", version="0.1.0")


class ExperimentCreate(BaseModel):
    name: str = Field(..., description="Experiment name")
    dataset: str = Field(..., description="Dataset identifier")
    teacher_model: str = Field(..., description="Teacher model id")
    student_model: str = Field(..., description="Student model id")
    assistant_search_space: str = Field(..., description="Teacher assistant search space id")
    search_episodes: int = Field(20, ge=1, description="Number of ENAS search episodes")
    ta_training_epochs: int = Field(5, ge=1, description="Training epochs for each assistant candidate")
    seed: Optional[int] = Field(None, description="Optional random seed for reproducibility")

    @validator("name", "dataset", "teacher_model", "student_model", "assistant_search_space")
    def _non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Value cannot be empty")
        return value


class Experiment(BaseModel):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime
    details: ExperimentCreate
    latest_metrics: Dict[str, float] = Field(default_factory=dict)
    notes: Optional[str] = None


class ExperimentStatusUpdate(BaseModel):
    status: str = Field(..., description="New status for the experiment")
    notes: Optional[str] = Field(None, description="Optional human-readable note")
    metrics: Optional[Dict[str, float]] = Field(
        None, description="Optional metrics payload (e.g., accuracy, latency)"
    )

    @validator("status")
    def _status_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Status cannot be empty")
        return value


_EXPERIMENTS: Dict[str, Experiment] = {}
_EXPERIMENTS_LOCK = Lock()


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


@app.get("/experiments", response_model=List[Experiment])
def list_experiments():
    """Return all known experiments."""
    return list(_EXPERIMENTS.values())


@app.post("/experiments", response_model=Experiment, status_code=201)
def create_experiment(payload: ExperimentCreate):
    """Create a new experiment definition and store it in memory."""
    experiment_id = str(uuid4())
    now = datetime.utcnow()
    experiment = Experiment(
        id=experiment_id,
        status="created",
        created_at=now,
        updated_at=now,
        details=payload,
    )
    with _EXPERIMENTS_LOCK:
        _EXPERIMENTS[experiment_id] = experiment
    return experiment


@app.get("/experiments/{experiment_id}", response_model=Experiment)
def get_experiment(experiment_id: str):
    try:
        return _EXPERIMENTS[experiment_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Experiment not found")


@app.patch("/experiments/{experiment_id}", response_model=Experiment)
def update_experiment_status(experiment_id: str, payload: ExperimentStatusUpdate):
    """Update the status, notes, or metrics for an experiment."""
    with _EXPERIMENTS_LOCK:
        if experiment_id not in _EXPERIMENTS:
            raise HTTPException(status_code=404, detail="Experiment not found")
        experiment = _EXPERIMENTS[experiment_id]
        updated_fields = experiment.copy(update={
            "status": payload.status,
            "updated_at": datetime.utcnow(),
            "notes": payload.notes if payload.notes is not None else experiment.notes,
            "latest_metrics": payload.metrics
            if payload.metrics is not None
            else experiment.latest_metrics,
        })
        _EXPERIMENTS[experiment_id] = updated_fields
        return updated_fields
