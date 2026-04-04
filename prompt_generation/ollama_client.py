from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx

from prompt_generation.config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT_S


async def chat_completion(
    system: str,
    user: str,
    *,
    model: str | None = None,
    temperature: float = 0.2,
) -> str:
    """Call Ollama /api/chat and return assistant message content."""
    m = model or OLLAMA_MODEL
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload: dict[str, Any] = {
        "model": m,
        "stream": False,
        "options": {"temperature": temperature},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT_S) as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()
    msg = data.get("message") or {}
    content = msg.get("content")
    if not content:
        raise RuntimeError(f"Unexpected Ollama response: {json.dumps(data)[:500]}")
    return content.strip()


async def ollama_health() -> dict[str, Any]:
    url = f"{OLLAMA_BASE_URL}/api/tags"
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()


def load_canonical_structure() -> str:
    root = Path(__file__).resolve().parent.parent
    path = root / "data" / "canonical_prompt_structure.md"
    return path.read_text(encoding="utf-8")
