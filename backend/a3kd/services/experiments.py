import random
import threading
import time
from typing import Dict, List, Optional

from a3kd.models.domain import AssistantSummary, Experiment, ExperimentConfig, MetricsLog, ModelInfo


TEACHER_MODELS = [
    ModelInfo(id="resnet110", name="ResNet110 (teacher, CIFAR-100)"),
]

STUDENT_MODELS = [
    ModelInfo(id="resnet8", name="ResNet8 (student, CIFAR-100)"),
]


class ExperimentService:
    def __init__(self) -> None:
        self._experiments: Dict[str, Experiment] = {}
        self._metrics: Dict[str, MetricsLog] = {}
        self._assistants: Dict[str, AssistantSummary] = {}
        self._lock = threading.Lock()
        self._counter = 0

    def list_teachers(self) -> List[ModelInfo]:
        return TEACHER_MODELS

    def list_students(self) -> List[ModelInfo]:
        return STUDENT_MODELS

    def list_experiments(self) -> List[Experiment]:
        with self._lock:
            return list(self._experiments.values())

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        with self._lock:
            return self._experiments.get(experiment_id)

    def get_metrics(self, experiment_id: str) -> Optional[MetricsLog]:
        with self._lock:
            return self._metrics.get(experiment_id)

    def get_best_assistant(self, experiment_id: str) -> Optional[AssistantSummary]:
        with self._lock:
            return self._assistants.get(experiment_id)

    def create_experiment(self, config: ExperimentConfig) -> Experiment:
        with self._lock:
            self._counter += 1
            exp_id = f"exp_{self._counter}"
            experiment = Experiment(id=exp_id, config=config, status="running")
            self._experiments[exp_id] = experiment
            self._metrics[exp_id] = MetricsLog()

        worker = threading.Thread(target=self._run_experiment, args=(experiment,), daemon=True)
        worker.start()
        return experiment

    def _run_experiment(self, experiment: Experiment) -> None:
        for episode in range(1, experiment.config.search_episodes + 1):
            time.sleep(0.05)  # simulate compute
            ta_arch = self._sample_ta_architecture()
            acc = self._simulate_student_accuracy(episode)
            latency = self._simulate_latency()
            size = self._simulate_params()
            reward = self._compute_reward(acc, latency, size)

            self._log_metrics(experiment.id, episode, acc, reward)
            self._maybe_update_best(experiment.id, ta_arch, acc, latency, size)

        with self._lock:
            exp = self._experiments[experiment.id]
            exp.status = "completed"
            exp.best_accuracy = self._assistants[experiment.id].val_accuracy if experiment.id in self._assistants else 0.0

    def _sample_ta_architecture(self) -> str:
        choices = ["ta_resnet14", "ta_resnet20", "ta_resnet26"]
        return random.choice(choices)

    def _simulate_student_accuracy(self, episode: int) -> float:
        base = 0.45
        improvement = min(0.4, episode * 0.02)
        noise = random.uniform(-0.01, 0.02)
        return round(base + improvement + noise, 4)

    def _simulate_latency(self) -> float:
        return round(random.uniform(3.0, 6.0), 2)

    def _simulate_params(self) -> float:
        return round(random.uniform(2.5, 5.5), 2)

    def _compute_reward(self, acc: float, latency: float, size: float) -> float:
        reward = 0.6 * acc + 0.2 / (1 + latency) + 0.2 / (1 + size)
        return round(reward, 4)

    def _log_metrics(self, experiment_id: str, episode: int, acc: float, reward: float) -> None:
        with self._lock:
            metrics = self._metrics[experiment_id]
            metrics.episodes.append(episode)
            metrics.student_accuracy.append(acc)
            metrics.reward.append(reward)

    def _maybe_update_best(self, experiment_id: str, ta_arch: str, acc: float, latency: float, size: float) -> None:
        with self._lock:
            current_best = self._assistants.get(experiment_id)
            if current_best is None or acc > current_best.val_accuracy:
                summary = AssistantSummary(
                    architecture_id=ta_arch,
                    params_m=size,
                    latency_ms=latency,
                    val_accuracy=acc,
                )
                self._assistants[experiment_id] = summary
                self._experiments[experiment_id].best_accuracy = acc
                self._experiments[experiment_id].best_assistant_id = ta_arch
