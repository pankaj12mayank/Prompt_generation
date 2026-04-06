"""Run the web UI: python launch.py"""

import uvicorn
from prompt_generation.config import PORT

if __name__ == "__main__":
    uvicorn.run(
        "pg_ui.app:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
    )
