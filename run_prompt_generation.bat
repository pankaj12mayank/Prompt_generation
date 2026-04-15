@echo off
setlocal EnableExtensions
cd /d "%~dp0"

title Prompt Generation

echo.
echo ============================================================
echo   Prompt Generation 
echo   Ollama master-prompt UI
echo ------------------------------------------------------------
echo   Uses PORT from .env as the first port to try.
echo   If that port is busy ^(other projects^), the next free port is used.
echo   launch.py prints the real URL and can open your browser.
echo ------------------------------------------------------------

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Virtual environment not found.
  echo Create it from this folder:
  echo   python -m venv .venv
  echo   .venv\Scripts\pip install -r requirements.txt
  echo.
  pause
  exit /b 1
)

call .venv\Scripts\activate.bat
if errorlevel 1 (
  echo ERROR: Could not activate .venv
  pause
  exit /b 1
)

REM Avoid double browser: launch.py opens the correct port (including auto-pick).
set PROMPT_GEN_NO_BROWSER=0

echo Starting...  (Ctrl+C to stop)
echo.
python launch.py
echo.
pause
