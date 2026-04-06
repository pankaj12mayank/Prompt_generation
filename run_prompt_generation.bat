@echo off
setlocal EnableExtensions
cd /d "%~dp0"

title Prompt Generation

echo.
echo ============================================================
echo   Prompt Generation 
echo   Ollama master-prompt UI
echo ------------------------------------------------------------
echo   Open in your browser AFTER the server starts:
echo.
echo     http://127.0.0.1:8765
echo     http://localhost:8765
echo.
echo ============================================================
echo.

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

REM Open browser shortly after uvicorn begins listening
start "PromptGen-open-browser" cmd /c "timeout /t 3 /nobreak >nul && start http://127.0.0.1:8765/"

echo Starting uvicorn...  (Ctrl+C to stop)
echo.
python launch.py
echo.
pause
