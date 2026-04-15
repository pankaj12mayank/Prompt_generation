"""Run the web UI: python launch.py

Reads PORT from .env as the first port to try. If it is already in use (other
projects), the next free port is used automatically. Set PROMPT_GEN_NO_BROWSER=1
to skip opening a browser window.
"""

from __future__ import annotations

import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parent


def _find_listen_port(start: int, attempts: int = 64) -> int:
    for port in range(start, start + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("0.0.0.0", port))
            except OSError:
                continue
            return port
    raise SystemExit(
        f"No free TCP port in range {start}..{start + attempts - 1}. "
        "Close other apps using those ports or set a higher PORT in .env.\n"
    )


def _maybe_open_browser(url: str) -> None:
    if os.getenv("PROMPT_GEN_NO_BROWSER", "").strip() in ("1", "true", "yes"):
        return

    def _open() -> None:
        time.sleep(1.5)
        try:
            webbrowser.open(url)
        except Exception:
            pass

    threading.Thread(target=_open, daemon=True).start()


if __name__ == "__main__":
    load_dotenv(_REPO_ROOT / ".env")
    preferred = int(os.getenv("PORT", "8765"))
    listen_port = _find_listen_port(preferred)
    os.environ["LISTEN_PORT"] = str(listen_port)

    url = f"http://127.0.0.1:{listen_port}/"
    if listen_port != preferred:
        print(
            f"PORT {preferred} from .env is busy (another app may be using it).\n"
            f"Listening on {listen_port} instead. Open: {url}\n"
            f"(Change PORT in .env only when you want a different *preferred* port.)\n"
        )
    else:
        print(f"Prompt Generation -> {url}  (PORT from .env)\n")

    _maybe_open_browser(url)

    uvicorn.run(
        "pg_ui.app:app",
        host="0.0.0.0",
        port=listen_port,
        reload=False,
    )
