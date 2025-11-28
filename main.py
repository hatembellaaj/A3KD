"""Entry point for running the FastAPI app without Docker.

This file forwards to `a3kd.api.main:app` while ensuring the backend
package is on the Python path when executed from the repository root.
"""
from pathlib import Path
import sys

backend_path = Path(__file__).parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.append(str(backend_path))

from a3kd.api.main import app  # noqa: E402

__all__ = ["app"]
