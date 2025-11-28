# A3KD – Minimal Dockerized Platform

This project provides a **minimal A3KD platform**:

- Python + FastAPI backend (port 8000)
- React frontend in English (port 3000)
- Docker + docker-compose

## Install & Run

1. Install Docker and docker-compose.
2. Clone the repo:
   ```bash
   git clone https://github.com/your-org/a3kd-minimal.git
   cd a3kd-minimal
   ```

Build and start:

```bash
docker compose up --build
```

Open:

- API: <http://localhost:8000/docs>
- UI: <http://localhost:3000>

## How to Use (Example)

Open the web UI.

Click "New Experiment".

Fill the form:

- Experiment name: cifar100_example
- Dataset: CIFAR-100
- Teacher: ResNet110
- Student: ResNet8
- Search episodes: 10

Click "Create & Start".

The experiment appears on the dashboard. You can click it to see student accuracy per episode and the best assistant (architecture, latency, size).
