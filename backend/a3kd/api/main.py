from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from a3kd.models.domain import ExperimentConfig, ModelInfo
from a3kd.services.experiments import ExperimentService

app = FastAPI(title="A3KD Minimal API", version="0.1.0")
service = ExperimentService()


class ExperimentCreate(BaseModel):
    name: str
    dataset: str
    teacher_id: str
    student_id: str
    search_episodes: int = Field(gt=0, le=200)


class ExperimentResponse(BaseModel):
    experiment_id: str
    status: str


class ExperimentListItem(BaseModel):
    id: str
    name: str
    dataset: str
    teacher_id: str
    student_id: str
    status: str
    best_accuracy: float


class ExperimentDetail(BaseModel):
    id: str
    config: ExperimentConfig
    status: str
    best_accuracy: float
    best_assistant_id: str | None


class MetricsResponse(BaseModel):
    episodes: list[int]
    student_accuracy: list[float]
    reward: list[float]


class AssistantResponse(BaseModel):
    architecture_id: str
    params_m: float
    latency_ms: float
    val_accuracy: float


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/models/teachers", response_model=list[ModelInfo])
def list_teachers() -> list[ModelInfo]:
    return service.list_teachers()


@app.get("/models/students", response_model=list[ModelInfo])
def list_students() -> list[ModelInfo]:
    return service.list_students()


@app.post("/experiments", response_model=ExperimentResponse, status_code=201)
def create_experiment(payload: ExperimentCreate) -> ExperimentResponse:
    config = ExperimentConfig(
        name=payload.name,
        dataset=payload.dataset,
        teacher_id=payload.teacher_id,
        student_id=payload.student_id,
        search_episodes=payload.search_episodes,
    )
    experiment = service.create_experiment(config)
    return ExperimentResponse(experiment_id=experiment.id, status=experiment.status)


@app.get("/experiments", response_model=list[ExperimentListItem])
def list_experiments() -> list[ExperimentListItem]:
    experiments = service.list_experiments()
    return [
        ExperimentListItem(
            id=exp.id,
            name=exp.config.name,
            dataset=exp.config.dataset,
            teacher_id=exp.config.teacher_id,
            student_id=exp.config.student_id,
            status=exp.status,
            best_accuracy=exp.best_accuracy,
        )
        for exp in experiments
    ]


@app.get("/experiments/{experiment_id}", response_model=ExperimentDetail)
def get_experiment(experiment_id: str) -> ExperimentDetail:
    experiment = service.get_experiment(experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return ExperimentDetail(
        id=experiment.id,
        config=experiment.config,
        status=experiment.status,
        best_accuracy=experiment.best_accuracy,
        best_assistant_id=experiment.best_assistant_id,
    )


@app.get("/experiments/{experiment_id}/metrics", response_model=MetricsResponse)
def get_metrics(experiment_id: str) -> MetricsResponse:
    metrics = service.get_metrics(experiment_id)
    if metrics is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return MetricsResponse(
        episodes=metrics.episodes,
        student_accuracy=metrics.student_accuracy,
        reward=metrics.reward,
    )


@app.get("/experiments/{experiment_id}/best-assistant", response_model=AssistantResponse)
def get_best_assistant(experiment_id: str) -> AssistantResponse:
    assistant = service.get_best_assistant(experiment_id)
    if assistant is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return AssistantResponse(
        architecture_id=assistant.architecture_id,
        params_m=assistant.params_m,
        latency_ms=assistant.latency_ms,
        val_accuracy=assistant.val_accuracy,
    )
