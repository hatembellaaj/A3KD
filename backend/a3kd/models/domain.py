from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ModelInfo:
    id: str
    name: str


@dataclass
class ExperimentConfig:
    name: str
    dataset: str
    teacher_id: str
    student_id: str
    search_episodes: int


@dataclass
class Experiment:
    id: str
    config: ExperimentConfig
    status: str
    best_accuracy: float = 0.0
    best_assistant_id: Optional[str] = None


@dataclass
class MetricsLog:
    episodes: List[int] = field(default_factory=list)
    student_accuracy: List[float] = field(default_factory=list)
    reward: List[float] = field(default_factory=list)


@dataclass
class AssistantSummary:
    architecture_id: str
    params_m: float
    latency_ms: float
    val_accuracy: float
