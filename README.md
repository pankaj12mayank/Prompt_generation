# Prompt Generation

Local web app that turns rough project notes into a single **master agent prompt** (consulting-style BRD/FRD package instructions). Uses **Ollama** only (no paid API).

## Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) running locally with a capable model, for example:

```bash
ollama pull llama3.2
```

## Setup

```bash
cd Prompt_generation
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` if needed (`OLLAMA_MODEL`, `OLLAMA_BASE_URL`).

## Run

**Windows:** double-click `run_prompt_generation.bat` in this folder (uses `.venv`). The window prints the app URL; the browser opens to **http://127.0.0.1:8765** after a short delay.

This project uses **port 8765** only. *Master_agent* is a different app and typically uses **port 8000** — do not mix the two.

```bash
python launch.py
```

Open [http://127.0.0.1:8765](http://127.0.0.1:8765). Enter customer fields or paste rough notes, then **Generate master prompt**. Copy the Markdown into your downstream agent.

## API

- `GET /api/health` — Ollama reachability and installed models
- `POST /api/generate` — JSON body with the same field names as the form

## Docker

Ollama must be reachable from the container (often `host.docker.internal` on Docker Desktop). Build and run:

```bash
docker build -t prompt-gen .
docker run -p 8765:8765 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 prompt-gen
```

## Structure

| Path | Role |
|------|------|
| `data/canonical_prompt_structure.md` | Canonical sections the model must preserve |
| `prompt_generation/builder.py` | System instructions + Ollama call |
| `pg_ui/app.py` | FastAPI app (package is `pg_ui`, not `web`, so it never loads another project’s `web.app`) |
| `pg_ui/templates/index.html` | Simple two-column UI |

The model is instructed to keep the canonical skeleton and embed your project context; it should not invent budgets or features when data is missing.

## Troubleshooting

**Port 8765 shows Master_agent (wizard / requirement generation)**  
You were hitting the wrong Python module: both projects used to expose `web.app`. This project now uses **`pg_ui.app`**. Stop all uvicorn windows, then start again from the `Prompt_generation` folder (`run_prompt_generation.bat` or `python launch.py`). The page title should read **Prompt Generation — Ollama**.

**http://localhost:8000 does nothing**  
Master_agent’s UI only runs while its server is up. From the `Master_agent` folder run `run_web.bat` (or `python -m uvicorn web.app:app --host 0.0.0.0 --port 8000`). That is a **separate** terminal from Prompt_generation.
