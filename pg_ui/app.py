from __future__ import annotations

import sys
from pathlib import Path

# Repo root on sys.path when running: uvicorn pg_ui.app:app (not `web` — avoids clash with Master_agent)
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from prompt_generation.builder import RoughInput, generate_master_prompt
from prompt_generation.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from prompt_generation.ollama_client import ollama_health

app = FastAPI(title="Prompt Generation", version="1.0.0")

_static = Path(__file__).parent / "static"
_templates = Path(__file__).parent / "templates"
if _static.is_dir():
    app.mount("/static", StaticFiles(directory=str(_static)), name="static")
templates = Jinja2Templates(directory=str(_templates))


class GenerateBody(BaseModel):
    role: str = Field(default="", max_length=1000)
    goal: str = Field(default="", max_length=5000)
    steps: str = Field(default="", max_length=10000)
    review: str = Field(default="", max_length=5000)
    output: str = Field(default="", max_length=5000)
    additional_context: str = Field(default="", max_length=16000)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "ollama_url": OLLAMA_BASE_URL,
            "ollama_model": OLLAMA_MODEL,
        },
    )


@app.get("/api/health")
async def health() -> JSONResponse:
    try:
        tags = await ollama_health()
        models = [m.get("name", "") for m in tags.get("models", [])]
        return JSONResponse(
            {
                "ok": True,
                "ollama_reachable": True,
                "ollama_url": OLLAMA_BASE_URL,
                "configured_model": OLLAMA_MODEL,
                "installed_models": models,
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "ok": False,
                "ollama_reachable": False,
                "ollama_url": OLLAMA_BASE_URL,
                "error": str(e),
            },
        )


@app.post("/api/generate")
async def generate(body: GenerateBody) -> JSONResponse:
    if not any(
        [
            body.role.strip(),
            body.goal.strip(),
            body.steps.strip(),
        ]
    ):
        raise HTTPException(
            status_code=400,
            detail="Provide at least Role, Goal, or Steps to generate a prompt.",
        )
    rough = RoughInput(
        role=body.role.strip(),
        goal=body.goal.strip(),
        steps=body.steps.strip(),
        review=body.review.strip(),
        output=body.output.strip(),
        additional_context=body.additional_context.strip(),
    )
    try:
        markdown = await generate_master_prompt(rough)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e}") from e
    return JSONResponse({"markdown": markdown})
