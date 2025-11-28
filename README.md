# A3KD Platform – Adaptive Architecture-Aware Assistant Knowledge Distillation

This repository provides a Dockerized platform to run **A3KD** experiments.

A3KD combines **Teacher-Assistant Knowledge Distillation (TAKD)** with
an **ENAS-style controller** and an **adaptive multi-objective reward**.
The controller automatically searches for the best Teacher Assistant (TA)
architecture by balancing:

- Student accuracy
- TA latency
- TA model size

The platform includes:

- A Python backend (PyTorch + FastAPI) for training and search
- A React web UI (English) to configure, run, and monitor experiments
- Docker images and a `docker-compose.yml` file for easy deployment

---

## 1. Architecture Overview

**Services**

- `backend` – REST API, A3KD/ENAS training code, experiment manager
- `frontend` – React UI served on port `3000`

**Data Layout**

- `experiments/` – JSON files with experiment configuration and logs
- `checkpoints/` – model weights for teacher, assistants, and students
- `data/` – datasets (e.g. CIFAR-100) downloaded on first run

---

## 2. Prerequisites

1. **Docker** >= 20.x
2. **docker-compose** >= 1.29 or Docker Compose v2
3. (Optional, recommended) **GPU support**
   - NVIDIA GPU + drivers
   - `nvidia-container-toolkit` installed

If you do not have a GPU, the platform can still run on CPU,
but training and search will be much slower.

---

## 3. Quick Start

### 3.1 Clone the repository

```bash
git clone https://github.com/your-org/a3kd-platform.git
cd a3kd-platform
```

### 3.2 Start the stack with Docker Compose

```bash
docker compose up --build
```

This will:

- Build the backend image and start it on port 8000
- Build the frontend image and start it on port 3000

Wait until the logs show that the backend is running on `http://0.0.0.0:8000`.

### 3.2.1 Run the lightweight API locally (port 8570)

If you want to try the API without Docker, you can start the bundled FastAPI
application directly on port **8570**:

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8570
```

Then open:

- Swagger docs: <http://localhost:8570/docs>
- Root endpoint: <http://localhost:8570/>

### 3.3 Open the Web UI

Open your browser at:

```
http://localhost:3000
```

You should see the A3KD Dashboard with an empty list of experiments.

---

## 4. Running Your First Experiment (Example)

This section provides a complete, step-by-step example using a predefined configuration.

### 4.1 Example Scenario

We will run A3KD on CIFAR-100 with:

- Teacher: ResNet110
- Student: ResNet8
- TA search space: ResNet-like assistants (e.g. ResNet20–ResNet32)
- 20 ENAS episodes (shortened for demonstration)

### 4.2 Using the Web UI

1. Go to the Dashboard.
2. Click on **"New Experiment"**.
3. Fill in the form:
   - Experiment name: `cifar100_a3kd_example`
   - Dataset: `CIFAR-100`
   - Teacher model: `ResNet110`
   - Student model: `ResNet8`
   - TA search space: `resnet_ta_space_v1`
   - Search episodes: `20`
   - TA training epochs: `5`
   - Student training epochs: `50`
   - Max latency (ms): `5.0`
   - Max model size (M params): `5.0`
   - Random seed: `42`
4. Click **"Create & Start"**.

The experiment will appear on the dashboard with status **Queued** then **Running**.

### 4.3 Monitoring Progress

Click on the experiment row to open Experiment Details. You will see:

- A chart of Student Accuracy vs Episode.
- A chart of Reward vs Episode.
- A chart or table of TA Latency / Model Size vs Episode.

The **Best Teacher Assistant** panel displays:

- Selected TA architecture (e.g. ResNet20)
- Validation accuracy
- Latency and model size

For a sufficiently large search budget, you should observe that A3KD converges
to an assistant architecture that improves student accuracy while satisfying
latency and size constraints.

### 4.4 Accessing Raw Metrics and Checkpoints

All artifacts are stored under:

- `experiments/EXP_ID/metrics.json`
- `checkpoints/EXP_ID/`

You can inspect these files on the host machine or copy them out of the container.

---

## 5. Command-Line Usage (Optional)

You can run an experiment directly from the backend container.

Open a shell in the backend container:

```bash
docker compose exec backend bash
```

Run the A3KD CLI with an example config:

```bash
python -m a3kd.experiments.runner \
  --config /app/example_configs/cifar100_resnet_a3kd.yaml
```

This will:

- Create a new experiment
- Run the ENAS-based search with adaptive reward
- Save all logs and models under `/app/experiments` and `/app/checkpoints`

---

## 6. Configuration Files

Experiment configs are standard YAML files. Example: `example_configs/cifar100_resnet_a3kd.yaml`:

```yaml
name: cifar100_a3kd_example
dataset: CIFAR-100
teacher_id: resnet110
student_id: resnet8
assistant_search_space_id: resnet_ta_space_v1

search:
  episodes: 20
  max_ta_epochs: 5
  max_student_epochs: 50

hardware:
  max_latency_ms: 5.0
  max_params_m: 5.0

seed: 42
```

You can create new configuration files by copying this example and adjusting the values.

---

## 7. Customization

To add new teacher or student models:

- Implement them under `a3kd/models/teacher.py` or `a3kd/models/student.py`.
- Register them in the model registry.

To change the TA search space:

- Edit `a3kd/models/ta_search_space.py`.

To modify the adaptive reward behavior:

- Update `a3kd/nas/reward.py`.

After making changes, rebuild the Docker images:

```bash
docker compose build
docker compose up
```

---

## 8. Stopping the Stack

To stop all containers:

```bash
docker compose down
```

To remove all containers, networks, and volumes (including data), add the `--volumes` flag:

```bash
docker compose down --volumes
```

---

## 9. License

Add your chosen license here (MIT, Apache 2.0, etc.).
