# A3KD – Minimal Dockerized Platform

This project provides a **minimal A3KD platform**:

- Python + FastAPI backend (port 8000)
- React frontend in English (port 3000)
- Docker + docker-compose

## Installation

### Quick start with Docker (recommended)
1. Install Docker and docker-compose.
2. Clone the repository:
   ```bash
   git clone https://github.com/your-org/a3kd-minimal.git
   cd a3kd-minimal
   ```
3. Build and start the stack:
   ```bash
   docker compose up --build
   ```
4. Open the services:
   - API docs: <http://localhost:8000/docs>
   - UI dashboard: <http://localhost:3000>

### Local (without Docker)
If you want to run the backend locally for development:
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install -r backend/requirements.txt
   ```
2. Start the FastAPI app from the repo root:
   ```bash
   uvicorn main:app --reload --port 8000
   ```
3. For the React frontend:
   ```bash
   cd frontend
   npm install
   npm start
   ```

## How to Use

### Through the web UI
1. Open <http://localhost:3000>.
2. Click **New Experiment**.
3. Fill the form:
   - Experiment name: e.g., `cifar100_example`
   - Dataset: `CIFAR-100`
   - Teacher: `ResNet110`
   - Student: `ResNet8`
   - Search episodes: e.g., `10`
4. Click **Create & Start**. The experiment will appear on the dashboard; click it to view metrics and the best assistant summary.

### Through the API
You can drive the backend directly with HTTP requests (FastAPI + JSON).

- Health check
  ```bash
  curl http://localhost:8000/health
  ```

- List available models
  ```bash
  curl http://localhost:8000/models/teachers
  curl http://localhost:8000/models/students
  ```

- Create an experiment
  ```bash
  curl -X POST http://localhost:8000/experiments \
    -H "Content-Type: application/json" \
    -d '{
      "name": "cifar100_a3kd_example",
      "dataset": "CIFAR-100",
      "teacher_id": "resnet110",
      "student_id": "resnet8",
      "search_episodes": 10
    }'
  ```

- Fetch experiments
  ```bash
  curl http://localhost:8000/experiments
  curl http://localhost:8000/experiments/exp_1
  curl http://localhost:8000/experiments/exp_1/metrics
  curl http://localhost:8000/experiments/exp_1/best-assistant
  ```

## Testing

### Backend unit & API tests (pytest)
1. From the repo root, install backend dev dependencies (see Local mode above).
2. Run all backend checks:
   ```bash
   pytest backend
   ```
   Suggested scenarios to cover (can be implemented with pytest + httpx/TestClient):
   - **Reward logic**: stable positive reward, increases with accuracy, improves with lower latency/size, and adaptive weight updates stay normalized.
   - **Latency measurement**: latency stays positive and relatively stable across repeated calls.
   - **Experiment lifecycle**: `create_experiment` returns an ID and creates config/logs; `load_experiment` returns the original config.
   - **API endpoints**: `/health`, `/models/teachers`, `/models/students`, `/experiments` (POST + validation), `/experiments` (GET list), `/experiments/{id}`, `/experiments/{id}/metrics`, `/experiments/{id}/best-assistant`.

### Frontend tests (React)
1. Install Node.js dependencies in `frontend/`:
   ```bash
   cd frontend
   npm install
   ```
2. Run the React test suite:
   ```bash
   npm test
   ```
   You can also perform manual UI checks:
   - Dashboard renders header/table/button in English.
   - Creating an experiment via the UI shows it on the dashboard with the expected status.
   - Form validation shows clear English errors (missing name, negative or zero search episodes).
   - Detail page shows config, metrics area, and Best Assistant section updating as episodes run.

### End-to-end & performance checks
- With the stack running (`docker compose up --build`), create experiments via the UI and confirm they appear in the API list.
- Let runs finish to verify metrics stop evolving and best accuracy aligns with the max student accuracy.
- Launch multiple experiments in parallel; ensure the API stays responsive (health OK) and each experiment keeps its own metrics.
- Measure response time for `GET /health` and `GET /experiments` (target < 200 ms locally).
- Simulate an error in the training loop (via a debug flag) to confirm experiments move to a `Failed`-style status without crashing the backend and that errors are logged.
