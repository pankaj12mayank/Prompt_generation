import os
from pathlib import Path

from dotenv import load_dotenv

# Repo root (parent of `prompt_generation/`) so PORT and keys load even when cwd differs.
_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")

PORT = int(os.getenv("PORT", "8765"))
# Set by launch.py to the actual bind port when PORT is busy; otherwise same as PORT.
LISTEN_PORT = int(os.getenv("LISTEN_PORT", str(PORT)))
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_TIMEOUT_S = float(os.getenv("OLLAMA_TIMEOUT_S", "300"))
