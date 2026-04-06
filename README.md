---

# Prompt Generation (Local Setup Guide)

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A local web application that converts rough project notes into a structured **Master Agent Prompt (BRD/FRD style)** using **Ollama**.
No paid APIs required. Everything runs locally.

---

## Features

* Converts unstructured notes into structured prompts
* Fully local (no external API calls)
* Simple web UI
* FastAPI backend
* Docker support

---

## Prerequisites

Make sure you have:

* Python 3.11+
* Ollama installed and running

### Install Ollama model

```bash
ollama pull llama3:latest
```

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Prompt_generation
```

---

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Mac/Linux**

```bash
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Setup environment variables

```bash
copy .env.example .env
```

Default configuration:

```env
PORT=8765
OLLAMA_MODEL=llama3:latest
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

---

## Running the Application

### Option 1 (Windows)

```bash
run_prompt_generation.bat
```

---

### Option 2 (Manual)

```bash
python launch.py
```

---

## Access the App

Open in browser:

```
http://127.0.0.1:8765
```

---

## Usage

1. Enter:

   * Project Title
   * Business Objective
   * Features / Notes

2. Click **Generate Master Prompt**

3. Copy the generated Markdown

4. Use it in your AI workflow

---

## API Endpoints

### Health Check

```http
GET /api/health
```

---

### Generate Prompt

```http
POST /api/generate
```

#### Request Body

```json
{
  "project_title": "Test Project",
  "business_objective": "Testing generation",
  "core_features": "Feature 1",
  "additional_notes": "Note"
}
```

---

## Docker Setup (Optional)

### Build image

```bash
docker build -t prompt-gen .
```

---

### Run container

```bash
docker run -p 8765:8765 \
-e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
prompt-gen
```

---

## Project Structure

```
Prompt_generation/
│
├── launch.py              # Entry point
├── builder.py            # Prompt generation logic
├── pg_ui/
│   └── app.py            # FastAPI backend
├── templates/
│   └── index.html        # UI
├── requirements.txt
├── .env
└── run_prompt_generation.bat
```

---

## Configuration

| Variable        | Description       | Default                                          |
| --------------- | ----------------- | ------------------------------------------------ |
| PORT            | App port          | 8765                                             |
| OLLAMA_MODEL    | Model name        | llama3:latest                                    |
| OLLAMA_BASE_URL | Ollama server URL | [http://127.0.0.1:11434](http://127.0.0.1:11434) |

---

## Troubleshooting

### App opens wrong UI

* Stop all running terminals
* Restart:

```bash
python launch.py
```

---

### Ollama not responding

```bash
curl http://127.0.0.1:11434
```

---

### Port already in use

Update `.env`:

```env
PORT=9000
```

---

## Quick Start

```text
1. Install Python + Ollama
2. Pull model (llama3)
3. Setup virtual environment
4. Install dependencies
5. Run the app
6. Open browser and generate prompt
```

---

## Verification Steps

1. Start Ollama:

```bash
ollama serve
```

2. Run app:

```bash
python launch.py
```

3. Open:

```
http://localhost:8765/
```

4. Generate a prompt and test the copy button

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## License

This project is licensed under the MIT License.

---

Here’s an **enhanced GitHub README add-on** with all the sections you asked for. You can paste this below your existing README.

---

## Screenshots

> Add your screenshots inside a `/docs/images` folder in your repo.

### Home Screen

![Home UI](docs/images/home.png)

### Generated Prompt Output

![Generated Output](docs/images/output.png)

### Copy Success State

![Copy State](docs/images/copy.png)

---

## Demo GIF

> Place your demo GIF inside `/docs/demo.gif`

![Demo](docs/demo.gif)

**Tip to create GIF:**

* Use tools like:

  * ScreenToGif (Windows)
  * Kap (Mac)
* Keep it under 10–15 seconds for GitHub performance

---

## Architecture Diagram

```text
User (Browser)
     │
     ▼
Frontend (HTML UI - templates/index.html)
     │
     ▼
FastAPI Backend (pg_ui/app.py)
     │
     ▼
Prompt Builder (builder.py)
     │
     ▼
Ollama API (localhost:11434)
     │
     ▼
LLM Model (llama3)
```

---

### Optional (Better Visual Diagram)

You can generate a diagram using tools like:

* draw.io
* Excalidraw
* Whimsical

Save it as:

```
docs/images/architecture.png
```

Then embed:

```md
![Architecture](docs/images/architecture.png)
```

---

## Deployment

### Option 1: Render (Quick Cloud Deployment)

1. Push code to GitHub
2. Go to [https://render.com](https://render.com)
3. Create **Web Service**
4. Configure:

* Build Command:

```bash
pip install -r requirements.txt
```

* Start Command:

```bash
python launch.py
```

* Environment Variables:

```
OLLAMA_BASE_URL=<your-ollama-server>
PORT=8765
```

Important:

* Render does NOT support local Ollama directly
* You must host Ollama separately (EC2 recommended)

---

### Option 2: AWS EC2 (Recommended for Ollama)

#### Step 1: Launch EC2

* Ubuntu 22.04
* t3.large or higher (for LLM performance)

---

#### Step 2: Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull llama3
```

---

#### Step 3: Run App

```bash
git clone <repo>
cd Prompt_generation

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python launch.py
```

---

#### Step 4: Open Ports

Allow in security group:

* 8765 (App)
* 11434 (Ollama)

---

#### Step 5: Update `.env`

```env
OLLAMA_BASE_URL=http://<EC2-IP>:11434
```

---

### Option 3: Internal Tool (Company Use)

Best setup:

* Backend: EC2 / Internal VM
* Ollama: Same machine or GPU server
* Access: VPN / Internal Network

Flow:

```text
Employee → Internal URL → FastAPI → Ollama → Response
```

---

## Production Improvements (Recommended)

* Add Nginx reverse proxy
* Use systemd to run app as service
* Add authentication (basic auth / SSO)
* Enable HTTPS

---

## Folder Structure for Assets

```text
docs/
│
├── images/
│   ├── home.png
│   ├── output.png
│   ├── copy.png
│   └── architecture.png
│
└── demo.gif
```

---

## Pro Tips

* Keep screenshots lightweight (<500KB)
* Use consistent resolution
* Blur sensitive data before uploading
* Use dark/light mode consistently




