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
    project_title: str = Field(default="", max_length=500)
    business_objective: str = Field(default="", max_length=8000)
    target_users: str = Field(default="", max_length=4000)
    core_features: str = Field(default="", max_length=8000)
    platform: str = Field(default="", max_length=500)
    budget_range: str = Field(default="", max_length=500)
    timeline_expectation: str = Field(default="", max_length=500)
    region_market: str = Field(default="", max_length=500)
    competitors: str = Field(default="", max_length=2000)
    tech_preference: str = Field(default="", max_length=2000)
    additional_notes: str = Field(default="", max_length=16000)


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
            body.project_title.strip(),
            body.business_objective.strip(),
            body.additional_notes.strip(),
            body.core_features.strip(),
        ]
    ):
        raise HTTPException(
            status_code=400,
            detail="Provide at least Project Title, Business Objective, Core Features, or Additional Notes.",
        )
    rough = RoughInput(
        project_title=body.project_title.strip(),
        business_objective=body.business_objective.strip(),
        target_users=body.target_users.strip(),
        core_features=body.core_features.strip(),
        platform=body.platform.strip(),
        budget_range=body.budget_range.strip(),
        timeline_expectation=body.timeline_expectation.strip(),
        region_market=body.region_market.strip(),
        competitors=body.competitors.strip(),
        tech_preference=body.tech_preference.strip(),
        additional_notes=body.additional_notes.strip(),
    )
    try:
        markdown = await generate_master_prompt(rough)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Ollama error: {e}") from e
    return JSONResponse({"markdown": markdown})
