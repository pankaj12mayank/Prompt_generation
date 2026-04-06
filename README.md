Here’s your **clean, beginner-friendly README** rewritten in a simple step-by-step flow so **anyone can set it up locally without confusion** 👇

---

# 🚀 Prompt Generation (Local Setup Guide)

This is a local web app that converts your rough project notes into a **structured master agent prompt (BRD/FRD style)** using **Ollama (no paid APIs required)**.

---

# 🧩 1. Prerequisites (Install First)

Make sure you have:

* ✅ Python **3.11+**
* ✅ Ollama installed and running

### Install model in Ollama:

```bash
ollama pull llama3:latest
```

---

# 📁 2. Project Setup (One-Time)

Open terminal and run:

```bash
cd Prompt_generation
python -m venv .venv
```

### Activate virtual environment:

**Windows:**

```bash
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
source .venv/bin/activate
```

---

### Install dependencies:

```bash
pip install -r requirements.txt
```

---

### Setup environment file:

```bash
copy .env.example .env
```

---

### Default `.env` (already configured):

```env
PORT=8765
OLLAMA_MODEL=llama3:latest
OLLAMA_BASE_URL=http://127.0.0.1:11434
```

👉 You can change **PORT or MODEL here anytime**

---

# ▶️ 3. Run the Application

### ✅ Easiest (Windows):

Double-click:

```bash
run_prompt_generation.bat
```

---

### ✅ Manual way:

```bash
python launch.py
```

---

# 🌐 4. Open in Browser

Go to:

```
http://127.0.0.1:8765
```

---

# ✍️ 5. How to Use

1. Enter:

   * Project Title
   * Business Objective
   * Features / Notes
2. Click **"Generate Master Prompt"**
3. Copy the generated Markdown
4. Use it in your downstream AI agent

---

# 🔌 6. API Usage (Optional)

### Health Check:

```bash
GET /api/health
```

### Generate Prompt:

```bash
POST /api/generate
```

Example body:

```json
{
  "project_title": "Test Project",
  "business_objective": "Testing generation",
  "core_features": "Feature 1",
  "additional_notes": "Note"
}
```

---

# 🐳 7. Run with Docker (Optional)

### Build:

```bash
docker build -t prompt-gen .
```

### Run:

```bash
docker run -p 8765:8765 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 prompt-gen
```

---

# 📂 8. Project Structure (Simple View)

| Folder/File            | Purpose                    |
| ---------------------- | -------------------------- |
| `launch.py`            | Starts the app             |
| `pg_ui/app.py`         | Backend (FastAPI)          |
| `templates/index.html` | UI                         |
| `builder.py`           | Prompt generation logic    |
| `.env`                 | Config (PORT, MODEL, etc.) |

---

# ⚙️ 9. Important Notes

✅ App runs on **PORT = 8765** (change in `.env` if needed)
✅ Uses **Ollama default port = 11434**
✅ Everything runs **locally (no internet required after setup)**

---

# 🛠️ 10. Troubleshooting

### ❌ Wrong UI / Another project opens

✔️ Stop all running terminals
✔️ Restart using:

```bash
python launch.py
```

---

### ❌ Ollama not working

Check:

```bash
curl http://127.0.0.1:11434
```

---

### ❌ Port already in use

Change in `.env`:

```env
PORT=9000
```

---

# ✅ Final Flow (Quick Summary)

```text
1. Install Python + Ollama
2. Pull model (llama3)
3. Setup venv + install requirements
4. Copy .env
5. Run app
6. Open browser → generate prompt
```

---
### How to verify
1. Ensure your Ollama is running ( ollama serve ).
2. Run the project using run_prompt_generation.bat or python launch.py .
3. Open http://localhost:8765/ in your browser.
4. Fill in the fields and click Generate Master Prompt .
5. Once generated, test the Copy button to see the success state.